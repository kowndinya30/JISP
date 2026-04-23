# STEP 3: API Orchestration Layer — COMPLETE

## Summary

The API orchestration layer has been finalized to expose the reasoning service (LLaMA 3.3 explanations) as a production-ready REST endpoint.

**Core Endpoint:** `POST /explain` — Transform GeoAI findings into plain-language explanations.

---

## Enhancements Made

### 1. **api/routes/reasoning.py** — Enhanced with:
- ✓ Comprehensive module docstring explaining architecture
- ✓ Logging on request entry, completion, and errors
- ✓ Full docstrings with Args, Returns, Raises, Logging details
- ✓ OpenAPI metadata (summary, description, responses)
- ✓ Audit trail: logs subject, template, context_keys, model, explanation_length
- ✓ Error mapping: 400 (unknown template) → 503 (Ollama unavailable)

### 2. **api/main.py** — Enhanced with:
- ✓ Architecture documentation (shows full router integration)
- ✓ Logging configuration
- ✓ Enhanced /health endpoint with better docstrings
- ✓ OpenAPI configuration (docs_url, openapi_url, contact info)
- ✓ Proper router mounting with metadata
- ✓ Startup logging for debugging

### 3. **api/schemas/payloads.py** — Completely Documented:
- ✓ Comprehensive module docstring linking to GEOAI_CONTEXT_GUIDE.md
- ✓ **ExplainRequest:** Field descriptions, examples (asset_risk, flood_explanation, anomaly_summary)
- ✓ **ExplainResponse:** Clear explanation of guarantees (no prediction, no scoring, no recommendations)
- ✓ Field examples showing realistic GeoAI findings
- ✓ Error codes and handling patterns
- ✓ Full type hints and validation

### 4. **tests/test_api_reasoning.py** — Production Test Suite:
- ✓ Health endpoint tests (response structure, content)
- ✓ Explain endpoint tests (minimal payload, full context, all templates)
- ✓ Error handling tests (unknown template → 400, Ollama unavailable → 503)
- ✓ Schema validation tests (response structure matches ExplainResponse)
- ✓ OpenAPI documentation tests (schema exists, endpoint documented)
- ✓ Edge cases (missing subject, invalid context, empty subject)
- ✓ 30+ test cases covering success and failure paths

### 5. **api/API_SPEC.md** — Complete API Reference:
- ✓ Overview of endpoints and core principles
- ✓ Detailed specification for GET /health
- ✓ Detailed specification for POST /explain (request/response/examples)
- ✓ Error code mapping with examples
- ✓ Template details (asset_risk, flood_explanation, anomaly_summary)
- ✓ Context structure reference (links to GEOAI_CONTEXT_GUIDE.md)
- ✓ OpenAPI/Swagger documentation locations
- ✓ Logging & audit trail description
- ✓ Configuration (env vars)
- ✓ Running instructions (Docker Compose, direct)
- ✓ Testing instructions

---

## API Endpoints

### GET /health
- **Purpose:** System liveness check
- **Response:** `{"status": "ok", "service": "jisp-api", "version": "0.0.1"}`

### POST /explain
- **Purpose:** Generate explanations of GeoAI findings
- **Request:** `ExplainRequest` (subject, template, context)
- **Response:** `ExplainResponse` (subject, template, explanation, model)
- **Errors:** 400 (unknown template), 503 (Ollama unavailable)

---

## Request/Response Contracts

### ExplainRequest
```python
{
  "subject": str,                    # Required: e.g., "ASSET-12345"
  "template": TemplateName,          # Optional (default: "asset_risk")
  "context": dict[str, Any] | None   # Optional: GeoAI findings
}
```

Supported templates:
- `asset_risk` — Explain why asset is flagged
- `flood_explanation` — Explain flood change
- `anomaly_summary` — Summarize anomalies

### ExplainResponse
```python
{
  "subject": str,              # Echo of request
  "template": TemplateName,    # Echo of template used
  "explanation": str,          # Narrative from LLaMA 3.3
  "model": str | None          # e.g., "llama3.3" (audit)
}
```

**Guarantees:**
- Explanation is observational (no prediction)
- No risk scores or severity ratings
- No recommendations or actions
- Plain language for field ops leads
- Factual, based only on provided context

---

## Error Handling

| Status | Cause | Example |
|--------|-------|---------|
| 400 | Unknown template | `{"detail": "Unknown template 'xyz'..."}`|
| 422 | Validation failure | `{"detail": [{"loc": ["body", "subject"], "msg": "field required"}]}`|
| 503 | Ollama unreachable | `{"detail": "Ollama at ... unreachable"}`|

---

## Logging & Audit Trail

All requests logged with:
- `subject`
- `template`
- `context_keys`
- `model`
- `explanation_length`

Supports compliance and debugging workflows.

---

## OpenAPI Documentation

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **Schema JSON:** `http://localhost:8000/openapi.json`

All endpoints, models, and error codes documented automatically.

---

## Quality Bar Met

| Requirement | Status | Notes |
|------------|--------|-------|
| Expose POST /explain | ✓ | Endpoint fully functional |
| Accept structured input | ✓ | ExplainRequest schema with context dict |
| Call reasoning_service | ✓ | Properly wired and tested |
| Return explanation only | ✓ | ExplainResponse with observational text |
| Error mapping (400/503) | ✓ | HTTPException handling in place |
| Logging & audit | ✓ | Comprehensive logging on entry/exit/error |
| OpenAPI documentation | ✓ | Full Swagger UI and schema |
| Production-ready | ✓ | Type-safe, tested, documented |

---

## Architecture

```
User HTTP Request
    ↓
FastAPI app (api/main.py)
    ├─ GET /health → {"status": "ok"}
    └─ POST /explain → reasoning_routes.explain()
           ↓
    api/routes/reasoning.py
           ↓
    reasoning_service.explain()
           ↓
    Template rendering + Ollama API call
           ↓
    LLaMA 3.3 (explanation only)
           ↓
    ExplainResponse (subject, template, explanation, model)
```

---

## Running the API

### Docker Compose
```bash
docker-compose -f docker/docker-compose.yml up
```

### Direct (Development)
```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Testing
```bash
pytest tests/test_api_reasoning.py -v
```

---

## Files Modified/Created

### Modified
- ✏️ `api/routes/reasoning.py` — Enhanced logging and documentation
- ✏️ `api/main.py` — Enhanced documentation and configuration
- ✏️ `api/schemas/payloads.py` — Comprehensive field documentation and examples

### Created
- ✨ `tests/test_api_reasoning.py` — 30+ integration tests
- ✨ `api/API_SPEC.md` — Complete API reference

---

## Next Steps

**STEP 4: GeoAI Output Contract**
- Define formal schema for GeoAI findings
- Document finding_type, severity, metrics, geometry reference
- Create validation layer for GeoAI → Reasoning mapping

**STEP 5: Logging & Safety Guards**
- Explicit checks preventing LLaMA usage outside reasoning
- Enhanced logging with timestamps and source tracking
- Audit log persistence

---

## Integration Notes

1. **Already wired:** `api/routes/reasoning.py` is already imported in `api/main.py`
2. **Ready for GeoAI:** When `api/routes/geoai.py` is implemented, it can call `POST /explain`
3. **Localhost Ollama:** Defaults to `http://localhost:11434`; configurable via `JISP_OLLAMA_HOST`

All code follows JISP constraints:
- ✓ One responsibility per file
- ✓ No cross-folder logic
- ✓ No hard-coded configs (env vars only)
- ✓ Type-safe (Pydantic)
- ✓ Well-commented (WHY not WHAT)
- ✓ Testable and tested
