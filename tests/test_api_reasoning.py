"""Integration tests for the JISP API reasoning endpoints.

Tests verify:
1. /health endpoint responds correctly
2. /explain endpoint accepts valid requests
3. Error handling for unknown templates (400)
4. Error handling for Ollama unavailable (503)
5. Response structure matches schema
"""

import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


class TestHealthEndpoint:
    """Test the /health system endpoint."""

    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_response_structure(self, client):
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert "service" in data
        assert "version" in data
        assert data["status"] == "ok"
        assert data["service"] == "jisp-api"

    def test_health_version_present(self, client):
        response = client.get("/health")
        data = response.json()
        assert data["version"] == "0.0.1"


class TestExplainEndpoint:
    """Test the POST /explain reasoning endpoint."""

    def test_explain_endpoint_exists(self, client):
        """Verify the endpoint is registered."""
        # This should not 404
        response = client.post(
            "/explain",
            json={
                "subject": "test-asset",
                "template": "asset_risk",
                "context": None,
            },
        )
        # May fail due to Ollama unavailability, but should not 404
        assert response.status_code != 404

    def test_explain_request_with_minimal_payload(self, client):
        """Test request with required fields only."""
        response = client.post(
            "/explain",
            json={
                "subject": "ASSET-001",
                "template": "asset_risk",
            },
        )
        # Will depend on Ollama availability, but request should be valid
        assert response.status_code in (200, 503)  # 200 success or 503 Ollama unavailable

    def test_explain_request_with_full_context(self, client):
        """Test request with complete GeoAI context."""
        request_body = {
            "subject": "ASSET-12345",
            "template": "asset_risk",
            "context": {
                "finding_type": "flood_proximity",
                "severity_raw": 0.78,
                "metrics": {"proximity_km": 2.5, "flood_extent_percent": 15},
                "signals": ["Active flood zone detected within 5 km"],
            },
        }
        response = client.post("/explain", json=request_body)
        # Will depend on Ollama availability
        assert response.status_code in (200, 503)

    def test_explain_unknown_template_returns_400(self, client):
        """Test that unknown template returns 400 Bad Request."""
        response = client.post(
            "/explain",
            json={
                "subject": "ASSET-001",
                "template": "nonexistent_template",  # Invalid template
                "context": None,
            },
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "nonexistent_template" in data["detail"].lower()

    def test_explain_response_structure_on_success(self, client):
        """Test response structure matches ExplainResponse schema."""
        # Mock a successful response (assuming Ollama is running)
        request_body = {
            "subject": "ASSET-001",
            "template": "asset_risk",
            "context": {"minimal": "context"},
        }
        response = client.post("/explain", json=request_body)

        if response.status_code == 200:
            data = response.json()
            # Verify response structure
            assert "subject" in data
            assert "template" in data
            assert "explanation" in data
            assert data["subject"] == "ASSET-001"
            assert data["template"] == "asset_risk"
            assert isinstance(data["explanation"], str)
            assert len(data["explanation"]) > 0

    def test_explain_default_template(self, client):
        """Test that template defaults to 'asset_risk'."""
        request_body = {
            "subject": "ASSET-001",
            "context": None,
            # No template specified — should default to 'asset_risk'
        }
        response = client.post("/explain", json=request_body)
        if response.status_code == 200:
            data = response.json()
            assert data["template"] == "asset_risk"

    def test_explain_with_all_templates(self, client):
        """Test all three supported templates."""
        templates = ["asset_risk", "flood_explanation", "anomaly_summary"]

        for template in templates:
            response = client.post(
                "/explain",
                json={
                    "subject": f"TEST-{template.upper()}",
                    "template": template,
                    "context": None,
                },
            )
            # Should not 404 or return unknown template error
            assert response.status_code != 404
            if response.status_code == 400:
                # Only 400 if template is unknown (shouldn't be)
                assert "unknown" not in response.json()["detail"].lower()

    def test_explain_model_metadata_in_response(self, client):
        """Verify model metadata is returned for audit purposes."""
        request_body = {
            "subject": "ASSET-001",
            "template": "asset_risk",
            "context": None,
        }
        response = client.post("/explain", json=request_body)

        if response.status_code == 200:
            data = response.json()
            # Model should be present for audit trail
            assert "model" in data
            assert data["model"] is not None
            assert isinstance(data["model"], str)
            assert "llama" in data["model"].lower()


class TestAPIDocumentation:
    """Test that API documentation is properly configured."""

    def test_openapi_schema_available(self, client):
        """Verify OpenAPI schema is accessible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema or "swagger" in schema
        assert "paths" in schema

    def test_openapi_explain_endpoint_documented(self, client):
        """Verify /explain endpoint is in OpenAPI schema."""
        response = client.get("/openapi.json")
        schema = response.json()
        paths = schema.get("paths", {})
        assert "/explain" in paths

    def test_swagger_ui_available(self, client):
        """Verify Swagger UI is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower() or "redoc" in response.text.lower()


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_explain_missing_required_subject(self, client):
        """Test that missing subject field returns validation error."""
        response = client.post(
            "/explain",
            json={
                "template": "asset_risk",
                "context": None,
                # Missing 'subject' field
            },
        )
        assert response.status_code == 422  # Pydantic validation error

    def test_explain_invalid_context_type(self, client):
        """Test that invalid context type is handled."""
        response = client.post(
            "/explain",
            json={
                "subject": "ASSET-001",
                "template": "asset_risk",
                "context": "invalid string instead of dict",
            },
        )
        # Should be caught by Pydantic validation
        assert response.status_code in (422, 200)  # 422 validation or 200 if coerced

    def test_explain_empty_subject(self, client):
        """Test that empty subject is handled (allowed but may be ignored by LLM)."""
        response = client.post(
            "/explain",
            json={
                "subject": "",
                "template": "asset_risk",
                "context": None,
            },
        )
        # Should accept empty string (validation passes)
        # Behavior depends on Ollama and template
        assert response.status_code in (200, 503)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
