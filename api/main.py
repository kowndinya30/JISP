"""JISP FastAPI entrypoint and application factory.

Current scope:
- System endpoints: /health
- Reasoning endpoints: /explain (LLaMA 3.3 explanation-only)

No database integration yet (STEP 4+).

Router modules:
- reasoning: POST /explain — transform GeoAI findings to plain-language explanations

Architecture:
    JISP API (/health, /explain)
        ├── Reasoning Layer (via reasoning_routes)
        │   ├── ollama_client: Calls Ollama /api/generate
        │   └── reasoning_service: Template → LLaMA → Explanation
        └── (Future: GeoAI Layer, Asset Layer, Timeseries Layer)

OpenAPI:
    Available at /docs (Swagger UI) and /openapi.json
"""

import logging

from fastapi import FastAPI

from api.routes import reasoning as reasoning_routes


# Configure module logger
logger = logging.getLogger(__name__)

# FastAPI application
app = FastAPI(
    title="JISP API",
    description=(
        "Jacobs Spatial Intelligence Platform — pre-field, AI-first, "
        "geospatial-native, explainable by design. "
        "\n\n"
        "**Current Scope:** Reasoning layer (LLaMA 3.3 explanations) for GeoAI findings. "
        "No prediction, no scoring — explanation only."
    ),
    version="0.0.1",
    docs_url="/docs",
    openapi_url="/openapi.json",
    contact={
        "name": "JISP Development",
        "url": "https://github.com/jacobs-spatial/jisp",
    },
)


@app.get(
    "/health",
    tags=["system"],
    summary="Health check",
    description="Verify the JISP API is running and healthy.",
    responses={200: {"description": "Service is healthy"}},
)
def health() -> dict[str, str]:
    """System health endpoint.

    Returns:
        Dictionary with service status, name, and version.
    """
    return {
        "status": "ok",
        "service": "jisp-api",
        "version": app.version,
    }


# Include routers
app.include_router(
    reasoning_routes.router,
    prefix="",
    tags=["reasoning"],
)

logger.info("JISP API initialized", extra={"version": app.version})
