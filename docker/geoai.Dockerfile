# JISP GeoAI container — GPU-capable minimal Ubuntu base.
#
# Per the JISP spec: GeoAI containers MUST be GPU-capable; base images
# must stay minimal; CPU must NOT be saturated. The `nvidia/cuda:*-base`
# variant is the smallest CUDA image (runtime only; no cuDNN, no dev
# toolkit) and is the right starting point.
#
# Not active in Step 4's compose stack. Real GeoAI deps
# (scikit-learn, PySAL, HDBSCAN, PyOpenCL / Numba, GDAL, GeoPandas,
# Rasterio, xarray, SHAP) are added alongside logic in a later step.

FROM nvidia/cuda:12.4.0-base-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Minimal Python toolchain. Geospatial / GeoAI packages land later.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3.11 python3.11-venv python3-pip ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Non-root runtime user (created with a home so pip --user works later).
RUN useradd --system --create-home --shell /usr/sbin/nologin jisp
USER jisp

# Placeholder entrypoint until GeoAI logic lands in a later step.
CMD ["python3.11", "-c", "print('jisp-geoai container up — awaiting logic')"]
