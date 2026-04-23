# JISP API container.
#
# The API is a thin HTTP layer — it forwards /explain requests to Ollama
# and will later forward DB / GeoAI calls to their respective services.
# GPU is NOT required here (heavy inference runs in the Ollama container).
#
# Build context: the repository root (see docker/docker-compose.yml).

FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install runtime deps first for better layer caching.
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy only the modules the API needs at runtime. Broad folders
# (`data/`, `docs/`, `tests/`, `ui/`, `scripts/`) are excluded via
# `.dockerignore` regardless.
COPY api/       ./api/
COPY reasoning/ ./reasoning/
COPY config/    ./config/

# Drop privileges — the API does not need root.
RUN useradd --system --create-home --shell /usr/sbin/nologin jisp
USER jisp

EXPOSE 8000

# Single worker is fine for local dev; compose overrides if needed.
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
