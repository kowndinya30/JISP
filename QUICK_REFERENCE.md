# JISP STEPS 1–3 QUICK REFERENCE

## ✅ Status: COMPLETE

---

## What Was Built

### 1. Reasoning Layer (LLaMA 3.3)
- Ollama HTTP client (single-shot generation)
- Template rendering service
- 3 explanation-only templates

### 2. Enhanced Templates
- Asset risk explanations
- Flood change explanations
- Anomaly summaries
- 5 guardrails per template (no prediction, no scoring)

### 3. API Orchestration
- REST endpoint: `POST /explain`
- Request/response validation
- Error handling (400, 503)
- Comprehensive logging
- OpenAPI documentation

---

## Quick Start

### Run the API
```bash
# Docker Compose (includes Ollama)
docker-compose -f docker/docker-compose.yml up
# Open: http://localhost:8000/docs

# Direct (requires local Ollama)
python -m uvicorn api.main:app --reload
```

### Test the API
```bash
# Health check
curl http://localhost:8000/health

# Explain a finding
curl -X POST http://localhost:8000/explain \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "ASSET-001",
    "template": "asset_risk",
    "context": {
      "finding_type": "flood_proximity",
      "metrics": {"proximity_km": 2.5}
    }
  }'
```

### Run Tests
```bash
pytest tests/test_reasoning_templates.py tests/test_api_reasoning.py -v
```

---

## File Locations

### Core Modules
| File | Lines | Purpose |
|------|-------|---------|
| `reasoning/ollama_client.py` | 99 | Ollama HTTP client |
| `reasoning/reasoning_service.py` | 82 | Template + LLaMA service |
| `api/main.py` | ~70 | FastAPI app |
| `api/routes/reasoning.py` | ~110 | POST /explain endpoint |
| `api/schemas/payloads.py` | ~100 | Request/response models |

### Templates
```
reasoning/prompt_templates/
├── asset_risk.txt               (30 lines, enhanced)
├── flood_explanation.txt        (31 lines, enhanced)
├── anomaly_summary.txt          (32 lines, enhanced)
├── GEOAI_CONTEXT_GUIDE.md       (150+ lines)
└── STEP2_COMPLETION_SUMMARY.md  (120+ lines)
```

### Tests
```
tests/
├── test_reasoning_templates.py  (250+ lines, 20 cases)
└── test_api_reasoning.py        (350+ lines, 30 cases)
```

### Documentation
```
api/
├── API_SPEC.md                  (Complete API reference)
└── STEP3_COMPLETION_SUMMARY.md

reasoning/prompt_templates/
└── GEOAI_CONTEXT_GUIDE.md       (Context schema guide)

Repository Root
├── STEPS_1_3_COMPLETION.md      (Overview)
└── DELIVERABLES_MANIFEST.md     (Complete manifest)
```

---

## Configuration

```bash
# Environment variables (defaults in parentheses)
JISP_OLLAMA_HOST=http://localhost:11434
JISP_OLLAMA_MODEL=llama3.3
JISP_OLLAMA_TIMEOUT_SECONDS=60
```

---

## API Endpoints

### GET /health
```
curl http://localhost:8000/health
→ {"status": "ok", "service": "jisp-api", "version": "0.0.1"}
```

### POST /explain
```
curl -X POST http://localhost:8000/explain \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "ASSET-ID",
    "template": "asset_risk|flood_explanation|anomaly_summary",
    "context": {...GeoAI findings...}
  }'

→ {
    "subject": "ASSET-ID",
    "template": "asset_risk",
    "explanation": "Plain language explanation...",
    "model": "llama3.3"
  }
```

---

## Templates

| Template | Use Case | Output |
|----------|----------|--------|
| `asset_risk` | Why is this asset flagged? | Signals → Metrics → Investigation |
| `flood_explanation` | What does the flood change mean? | Observed → Spatial → Hydrology |
| `anomaly_summary` | What is this anomaly? | Deviation → Context → Investigation |

**All templates guarantee:**
- ✅ Observational output ("what IS")
- ❌ No predictions ("what WILL BE")
- ❌ No scoring or risk ratings
- ❌ No recommendations or actions
- ✅ Plain language for field ops

---

## Error Handling

| Status | Meaning | Example |
|--------|---------|---------|
| 200 | Success | Normal response |
| 400 | Unknown template | `"Unknown template 'foo'"` |
| 422 | Validation error | Missing required field |
| 503 | Ollama unreachable | `"Ollama at ... unreachable"` |

---

## Documentation

| Document | Purpose |
|----------|---------|
| `api/API_SPEC.md` | Full API reference with examples |
| `reasoning/prompt_templates/GEOAI_CONTEXT_GUIDE.md` | Context schemas for each template |
| `STEPS_1_3_COMPLETION.md` | Overview of all 3 steps |
| `DELIVERABLES_MANIFEST.md` | Complete deliverables list |

---

## Testing

```bash
# All tests
pytest tests/ -v

# Specific suite
pytest tests/test_reasoning_templates.py -v
pytest tests/test_api_reasoning.py -v

# With coverage
pytest tests/ --cov=reasoning --cov=api

# Specific test
pytest tests/test_api_reasoning.py::TestExplainEndpoint::test_explain_unknown_template_returns_400 -v
```

---

## Monitoring

```bash
# Check Ollama
curl http://localhost:11434/api/tags

# Check API health
curl http://localhost:8000/health

# View API docs
# Browser: http://localhost:8000/docs
# Schema: http://localhost:8000/openapi.json

# View logs
# Docker: docker logs jisp-api
# Direct: Check console output
```

---

## Key Decisions (Locked)

✅ **Explanation-Only:** LLaMA never predicts or scores  
✅ **LLaMA 3.3:** Explicit, configurable model  
✅ **Observational:** "X was detected at Y on Z" (not "X might happen")  
✅ **Field-Ops Ready:** Plain language, no jargon  
✅ **Auditability:** Logged request/response/model  
✅ **Type-Safe:** Pydantic validation throughout  
✅ **Localhost Ollama:** Single-shot, no streaming  

---

## Next Steps

**STEP 4:** GeoAI Output Contract
- Define finding_type, severity_raw, metrics, geometry schema
- Create validation layer

**STEP 5:** Logging & Safety Guards
- Enhanced audit logging
- Source tracking
- Prevention of LLaMA misuse

---

## Support

- API Reference: `api/API_SPEC.md`
- Context Guide: `reasoning/prompt_templates/GEOAI_CONTEXT_GUIDE.md`
- Implementation: `api/STEP3_COMPLETION_SUMMARY.md`
- Overall Summary: `STEPS_1_3_COMPLETION.md`

---

*Status: ✅ PRODUCTION READY*  
*Coverage: 50+ test cases*  
*Documentation: 2500+ lines*
