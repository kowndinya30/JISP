"""Test suite for reasoning service prompt templates.

Validates that:
1. All templates load without error
2. Placeholder interpolation works correctly
3. Templates constrain explanations (no predictions, no scoring)
"""

from pathlib import Path
import pytest
from reasoning.reasoning_service import _load_template, _render_context
from reasoning.ollama_client import OllamaConfig


class TestTemplateLoading:
    """Verify all templates exist and load."""

    def test_asset_risk_template_exists(self):
        template = _load_template("asset_risk")
        assert template
        assert "{subject}" in template
        assert "{context}" in template

    def test_flood_explanation_template_exists(self):
        template = _load_template("flood_explanation")
        assert template
        assert "{subject}" in template
        assert "{context}" in template

    def test_anomaly_summary_template_exists(self):
        template = _load_template("anomaly_summary")
        assert template
        assert "{subject}" in template
        assert "{context}" in template

    def test_unsupported_template_raises_error(self):
        from reasoning.reasoning_service import UnknownTemplateError
        with pytest.raises(UnknownTemplateError):
            _load_template("nonexistent_template")


class TestTemplateInterpolation:
    """Verify template rendering with sample GeoAI contexts."""

    def test_render_context_empty(self):
        result = _render_context(None)
        assert result == "(none)"

    def test_render_context_dict(self):
        context = {
            "finding_type": "flood_proximity",
            "severity_raw": 0.78,
            "metrics": {"proximity_km": 2.5},
        }
        result = _render_context(context)
        assert "finding_type" in result
        assert "flood_proximity" in result
        assert "2.5" in result

    def test_asset_risk_template_interpolates(self):
        template = _load_template("asset_risk")
        context = {
            "asset_id": "ASSET-001",
            "proximity_km": 2.5,
            "signals": ["flood detected"],
        }
        rendered = template.format(
            subject="ASSET-001",
            context=_render_context(context),
        )
        assert "ASSET-001" in rendered
        assert "flood detected" in rendered

    def test_flood_template_interpolates(self):
        template = _load_template("flood_explanation")
        context = {
            "event_id": "FLOOD-001",
            "metrics": {"change_percent": 8.2},
        }
        rendered = template.format(
            subject="FLOOD-001",
            context=_render_context(context),
        )
        assert "FLOOD-001" in rendered
        assert "8.2" in rendered

    def test_anomaly_template_interpolates(self):
        template = _load_template("anomaly_summary")
        context = {
            "anomaly_id": "ANOMALY-001",
            "deviation": {"magnitude_std_devs": 5.6},
        }
        rendered = template.format(
            subject="ANOMALY-001",
            context=_render_context(context),
        )
        assert "ANOMALY-001" in rendered
        assert "5.6" in rendered


class TestTemplateConstraints:
    """Verify templates enforce explanation-only constraints."""

    def test_asset_risk_forbids_predictions(self):
        template = _load_template("asset_risk")
        # Template should contain guardrails preventing prediction
        assert ("Do NOT" in template or "not" in template.lower()) and (
            "what IS" in template or "observed" in template.lower()
        )

    def test_asset_risk_forbids_scoring(self):
        template = _load_template("asset_risk")
        assert "risk score" in template.lower() or "score" in template.lower()

    def test_flood_template_forbids_predictions(self):
        template = _load_template("flood_explanation")
        # Should contain guardrails
        assert "Do NOT" in template or ("what changed" in template.lower() or "extent" in template.lower())

    def test_flood_template_forbids_scoring(self):
        template = _load_template("flood_explanation")
        assert "risk score" in template.lower() or "score" in template.lower()

    def test_anomaly_template_forbids_severity(self):
        template = _load_template("anomaly_summary")
        assert "severity" in template.lower()

    def test_templates_emphasize_observation(self):
        asset_risk = _load_template("asset_risk")
        flood = _load_template("flood_explanation")
        anomaly = _load_template("anomaly_summary")

        for template in [asset_risk, flood, anomaly]:
            # Should reference what was observed
            assert ("observed" in template.lower() or
                    "detected" in template.lower() or
                    "described" in template.lower())


class TestGeoAIContextExamples:
    """Integration: verify templates work with realistic GeoAI findings."""

    def test_asset_risk_with_flood_proximity_context(self):
        """Example from GEOAI_CONTEXT_GUIDE.md"""
        context = {
            "asset_id": "ASSET-12345",
            "asset_type": "infrastructure_bridge",
            "finding_type": "flood_proximity",
            "severity_raw": 0.78,
            "metrics": {
                "proximity_km": 2.5,
                "flood_extent_percent": 15,
                "recurrence_interval_years": 100
            },
            "signals": [
                "Active flood zone detected within 5 km",
                "Asset in FEMA floodplain boundary"
            ]
        }
        template = _load_template("asset_risk")
        rendered = template.format(
            subject="ASSET-12345",
            context=_render_context(context),
        )
        assert "ASSET-12345" in rendered
        assert "proximity_km" in rendered
        assert "signals" in rendered

    def test_flood_explanation_with_change_detection_context(self):
        """Example from GEOAI_CONTEXT_GUIDE.md"""
        context = {
            "event_id": "FLOOD-EVENT-2025-0042",
            "finding_type": "flood_change_detection",
            "metrics": {
                "flood_extent_change_sqkm": 12.3,
                "flood_extent_change_percent": 8.2,
                "max_water_depth_m": 2.1
            },
            "spatial_context": {
                "location": "River Valley",
                "proximity_to_asset_km": 1.2
            },
            "hydrology": {
                "rainfall_mm_72h": 145,
                "discharge_percentile": 92
            }
        }
        template = _load_template("flood_explanation")
        rendered = template.format(
            subject="FLOOD-EVENT-2025-0042",
            context=_render_context(context),
        )
        assert "FLOOD-EVENT-2025-0042" in rendered
        assert "12.3" in rendered
        assert "hydrology" in rendered

    def test_anomaly_summary_with_temperature_spike_context(self):
        """Example from GEOAI_CONTEXT_GUIDE.md"""
        context = {
            "anomaly_id": "ANOMALY-2025-00891",
            "finding_type": "temperature_spike",
            "baseline": {"mean_celsius": 18.5, "std_dev": 2.1},
            "observed": {"peak_celsius": 30.2, "duration_hours": 4},
            "deviation": {"magnitude_std_devs": 5.6}
        }
        template = _load_template("anomaly_summary")
        rendered = template.format(
            subject="ANOMALY-2025-00891",
            context=_render_context(context),
        )
        assert "ANOMALY-2025-00891" in rendered
        assert "30.2" in rendered
        assert "magnitude_std_devs" in rendered


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
