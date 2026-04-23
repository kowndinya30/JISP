# JISP API Specification — STEP 3

## Overview

The JISP API is a FastAPI application that exposes:
1. **System endpoints** for health/liveness
2. **Reasoning endpoints** for transforming GeoAI findings into explanations

**Core Principle:** All responses are observational (explanation-only). No prediction, scoring, or recommendations are produced by this API.

---

## Base URL

```
http://localhost:8000
```

(Or as deployed; see `docker-compose.yml` for containerized setup.)

---

## Endpoints

### 1. GET /health

**Purpose:** System health check (readiness probe).

**Request:**
```
GET /health
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "service": "jisp-api",
  "version": "0.0.1"
}
```

**Use Cases:**
- Kubernetes liveness probe
- Docker health check
- Load balancer readiness validation

---

### 2. POST /explain

**Purpose:** Generate plain-language explanations of GeoAI findings.

**Request:**
```
POST /explain
Content-Type: application/json
```

**Request Body (ExplainRequest):**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `subject` | string | ✓ | — | Unique identifier (asset ID, event ID, anomaly ID, etc.). |
| `template` | string | ✗ | `"asset_risk"` | Template name: `asset_risk`, `flood_explanation`, or `anomaly_summary`. |
| `context` | object | ✗ | `null` | Structured GeoAI findings (metrics, signals, spatial context, etc.). |

**Example Request:**

```bash
curl -X POST http://localhost:8000/explain \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "ASSET-12345",
    "template": "asset_risk",
    "context": {
      "finding_type": "flood_proximity",
      "severity_raw": 0.78,
      "metrics": {
        "proximity_km": 2.5,
        "flood_extent_percent": 15
      },
      "signals": [
        "Active flood zone detected within 5 km",
        "Asset in FEMA floodplain boundary"
      ]
    }
  }'
```

**Response (200 OK):**

```json
{
  "subject": "ASSET-12345",
  "template": "asset_risk",
  "explanation": "Asset ASSET-12345 is 2.5 km from an active flood zone with current extent of 15%. The asset sits at elevation 12m in an area where peak water reached 8m, providing a 4m buffer. Nearby drainage patterns should be confirmed during field inspection.",
  "model": "llama3.3"
}
```

**Error Responses:**

| Status | Condition | Example |
|--------|-----------|---------|
| 400 | Unknown template | `{"detail": "Unknown template 'xyz'. Supported: asset_risk, flood_explanation, anomaly_summary."}` |
| 422 | Validation error (missing required fields) | `{"detail": [{"loc": ["body", "subject"], "msg": "field required"}]}` |
| 503 | Ollama unreachable | `{"detail": "Ollama at http://localhost:11434 unreachable: ..."}` |

---

## Templates

### Template: `asset_risk`

**Purpose:** Explain why an asset is flagged based on proximity, signals, or spatial conditions.

**Expected Context:**
- `finding_type`: e.g., "flood_proximity", "sensor_anomaly"
- `severity_raw`: Numeric raw signal (0–1)
- `metrics`: Key measurements (proximity_km, extent_percent, etc.)
- `signals`: List of triggering observations

**Response Characteristics:**
- Observational: Describes what signals triggered the flag
- Spatial: Explains asset proximity to risks
- Investigative: Notes factors the field team should verify
- **NOT:** No risk scores, no predictions, no recommendations

**Example:**
```json
{
  "subject": "BRIDGE-042",
  "template": "asset_risk",
  "context": {
    "finding_type": "flood_proximity",
    "metrics": {"proximity_km": 2.5, "flood_extent_percent": 15},
    "signals": ["Active flood zone detected"]
  }
}
```

---

### Template: `flood_explanation`

**Purpose:** Explain a flood change detection event.

**Expected Context:**
- `finding_type`: "flood_change_detection"
- `observation_window`: { "before": ISO8601, "after": ISO8601 }
- `metrics`: Change magnitude (sqkm, percent, depth_m)
- `spatial_context`: Location, elevation range, land cover
- `hydrology`: Rainfall, discharge, soil moisture

**Response Characteristics:**
- Observational: "Flood extent increased by 8% on date X"
- Spatial: Proximity to asset, terrain, land use
- Hydrological: Rainfall, discharge context (explanatory, not predictive)
- **NOT:** No future flood predictions, no severity ratings

**Example:**
```json
{
  "subject": "FLOOD-EVENT-2025-0042",
  "template": "flood_explanation",
  "context": {
    "finding_type": "flood_change_detection",
    "metrics": {"change_percent": 8.2, "depth_m": 2.1},
    "hydrology": {"rainfall_mm_72h": 145, "discharge_percentile": 92}
  }
}
```

---

### Template: `anomaly_summary`

**Purpose:** Summarize spatial or temporal anomalies.

**Expected Context:**
- `finding_type`: e.g., "temperature_spike", "vegetation_stress"
- `deviation`: Magnitude (std_devs, percent_change)
- `baseline`: Historical mean, std dev, period
- `temporal_context`: Wind, cloud cover, sun angle
- `spatial_context`: Terrain, land use, proximity to heat sources

**Response Characteristics:**
- Observational: "Temperature rose 12°C in 4 hours"
- Contextual: Environmental factors that may explain the anomaly
- Investigative: What the field team should examine
- **NOT:** No severity scores, no outcome predictions, no alarms

**Example:**
```json
{
  "subject": "ANOMALY-2025-00891",
  "template": "anomaly_summary",
  "context": {
    "finding_type": "temperature_spike",
    "deviation": {"magnitude_std_devs": 5.6},
    "temporal_context": {"cloud_cover_percent": 5, "wind_mps": 1.2}
  }
}
```

---

## Expected GeoAI Context Structures

See **reasoning/prompt_templates/GEOAI_CONTEXT_GUIDE.md** for detailed schemas and examples:

1. **Asset Risk Context** — proximity, severity_raw, metrics, signals
2. **Flood Explanation Context** — change metrics, spatial context, hydrology
3. **Anomaly Summary Context** — deviation, temporal/spatial context

All contexts are flexible JSON (no enforced schema at API level); the template rendering layer validates appropriateness.

---

## OpenAPI / Swagger

**Interactive Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Schema JSON: `http://localhost:8000/openapi.json`

All endpoints, request/response models, and error codes are documented in the OpenAPI schema.

---

## Logging & Audit Trail

Every `/explain` request is logged with:
- `subject`
- `template`
- `context_keys` (keys in the provided context)
- `model` (LLaMA version)
- `explanation_length`

Logs can be configured in `config/logging.yaml`.

---

## Error Handling

### 400 Bad Request
- **Cause:** Unknown template or malformed request
- **Example:** `{"detail": "Unknown template 'foo'. Supported: asset_risk, ..."}`
- **Action:** Check template name against supported list; validate request JSON

### 422 Unprocessable Entity
- **Cause:** Pydantic validation failure (missing field, wrong type)
- **Example:** `{"detail": [{"loc": ["body", "subject"], "msg": "field required"}]}`
- **Action:** Check required fields; ensure JSON types match schema

### 503 Service Unavailable
- **Cause:** Ollama unreachable or unresponsive
- **Example:** `{"detail": "Ollama at http://localhost:11434 unreachable: ..."`
- **Action:** Verify Ollama is running (`docker ps | grep ollama`); check `JISP_OLLAMA_HOST` env var

---

## Configuration

Environment variables (see `.env.example`):

```bash
# Ollama
JISP_OLLAMA_HOST=http://localhost:11434        # Default: localhost:11434
JISP_OLLAMA_MODEL=llama3.3                     # Default: llama3.3
JISP_OLLAMA_TIMEOUT_SECONDS=60                 # Default: 60

# FastAPI (when running api/main.py directly)
JISP_API_HOST=0.0.0.0                          # Default: 127.0.0.1
JISP_API_PORT=8000                             # Default: 8000
```

---

## Running the API

### Option 1: Docker Compose (Recommended)

```bash
docker-compose -f docker/docker-compose.yml up
```

API available at `http://localhost:8000`

### Option 2: Direct (Development)

```bash
cd JISP/
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

API available at `http://localhost:8000`

---

## Testing

```bash
# Run all API tests
pytest tests/test_api_reasoning.py -v

# Test specific endpoint
pytest tests/test_api_reasoning.py::TestExplainEndpoint -v

# With coverage
pytest tests/test_api_reasoning.py --cov=api --cov-report=term-missing
```

---

## Future Extensions

- **STEP 4:** GeoAI output contract & findings schema
- **STEP 5:** Logging safety guards & audit trail
- Additional templates (change-point, clustering, etc.)
- Database integration (assets, events, history)
- Async explanation generation (stream responses)

---

## Design Principles (LOCKED)

1. **Explanation Only:** No prediction, scoring, or recommendations in responses
2. **Auditability:** All requests logged; model metadata included
3. **Observational Language:** "What is, not what will be"
4. **Explainability:** Field ops leads understand findings without specialist knowledge
5. **Deterministic (except text):** All logic is deterministic; only explanation text is from LLM

---

## Contact & Support

See `README.md` and `docs/` for architecture details.
