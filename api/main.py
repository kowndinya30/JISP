"""JISP FastAPI entrypoint.

Current scope: `/health` and `/explain`. No database.
`/explain` is wired to `reasoning.reasoning_service` (Ollama + Llama 3.3);
see `api/routes/reasoning.py`.
"""

from fastapi import FastAPI

from api.routes import reasoning as reasoning_routes

app = FastAPI(
    title="JISP API",
    description=(
        "Jacobs Spatial Intelligence Platform — pre-field, AI-first, "
        "geospatial-native, explainable by design."
    ),
    version="0.0.1",
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "jisp-api", "version": app.version}


app.include_router(reasoning_routes.router)
