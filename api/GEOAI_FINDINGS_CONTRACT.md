# GeoAI Findings Contract – STEP 4

## Overview

This document specifies the **formal contract** between GeoAI analysis modules and the reasoning layer (STEP 3). All GeoAI outputs MUST conform to one of the finding types defined here to be routed to the appropriate reasoning template.

---

## Core Principles

1. **Observable Only:** Findings describe deterministic, measured phenomena. No prediction, no ML scores, no probabilities.
2. **Structured Metrics:** Raw values only (km, %, m, degrees, etc.). No derived indices or alarm levels.
3. **Traceable Geometry:** All spatial findings reference WKT or GeoJSON coordinates for PostGIS integration.
4. **Finding-Type Routing:** Each finding type maps to exactly one reasoning template:
   - `flood_proximity` → `asset_risk.txt`
   - `flood_change_detection` → `flood_explanation.txt`
   - `temperature_spike`, `vegetation_anomaly` → `anomaly_summary.txt`
5. **Audit Trail:** Every finding includes timestamp and clear source identifiers.

---

## Finding Type: `flood_proximity`

### Purpose

Asset or location is in spatial proximity to an active or potential flood zone.

### Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `finding_type` | string | ✓ | Must be exactly `"flood_proximity"` |
| `asset_id` | string | ✗ | Unique asset identifier (e.g., `"ASSET-12345"`) |
| `asset_type` | string | ✗ | Classification (e.g., `"infrastructure_bridge"`, `"utility_station"`) |
| `severity_raw` | SeverityRaw | ✓ | Observable proximity measure (0.0–1.0 normalized) |
| `metrics` | object | ✓ | Raw spatial measurements (see table below) |
| `signals` | array[string] | ✗ | Observable conditions that triggered this finding |
| `geometry_reference` | GeometryReference | ✗ | WKT or GeoJSON point location of asset |
| `timestamp` | ISO 8601 | ✗ | When this finding was generated |

### Severity_raw Interpretation

- **Value:** Normalized 0.0–1.0
- **Percentile:** Optional historical rank (0–100)
- **Unit Description:** E.g., "distance to active flood zone as fraction of floodplain width"
- **Example:** `0.78` = asset is at 78th percentile of proximity risk (in historical context) among similar assets

### Metrics Fields (Examples)

| Metric | Type | Unit | Notes |
|--------|------|------|-------|
| `proximity_km` | float | km | Distance from asset center to nearest flood boundary |
| `flood_extent_percent` | float | % | Current flood extent as % of floodplain area |
| `recurrence_interval_years` | float | years | Return period of nearest flood zone (e.g., 100-year event) |
| `elevation_m` | float | m | Asset elevation above datum |
| `highest_historical_depth_m` | float | m | Maximum water depth recorded in this area |
| `buffer_m` | float | m | Vertical buffer (elevation minus historical high water) |
| `fema_zone` | string | — | FEMA floodplain designation (e.g., "AE", "X") |

### Example Payload

```json
{
  "finding_type": "flood_proximity",
  "asset_id": "ASSET-12345",
  "asset_type": "infrastructure_bridge",
  "severity_raw": {
    "value": 0.78,
    "percentile": 85,
    "unit_description": "distance to active flood zone as fraction of floodplain width"
  },
  "metrics": {
    "proximity_km": 2.5,
    "flood_extent_percent": 15,
    "recurrence_interval_years": 100,
    "elevation_m": 12,
    "highest_historical_depth_m": 8,
    "buffer_m": 4,
    "fema_zone": "AE"
  },
  "signals": [
    "Active flood zone detected within 5 km",
    "Asset in FEMA floodplain boundary (1% annual chance)",
    "Elevation 12m; historical high water 8m"
  ],
  "geometry_reference": {
    "format": "wkt",
    "value": "POINT(-73.9352 40.7306)"
  },
  "timestamp": "2025-03-15T10:30:00Z"
}
```

---

## Finding Type: `flood_change_detection`

### Purpose

Flood extent or depth changed measurably over a specified time window.

### Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `finding_type` | string | ✓ | Must be exactly `"flood_change_detection"` |
| `event_id` | string | ✗ | Unique flood event identifier (e.g., `"FLOOD-EVENT-2025-0042"`) |
| `observation_window` | object | ✓ | Time window with `"before"` and `"after"` (ISO 8601) |
| `severity_raw` | SeverityRaw | ✓ | Observable intensity of change (0.0–1.0 normalized) |
| `metrics` | object | ✓ | Raw measurements of extent/depth change (see table below) |
| `spatial_context` | object | ✗ | Geographic factors (location, elevation range, land cover) |
| `hydrology` | object | ✗ | Hydrological drivers (rainfall, discharge percentile) |
| `timestamp` | ISO 8601 | ✗ | When this finding was generated |

### Severity_raw Interpretation

- **Value:** Normalized 0.0–1.0 representing change magnitude relative to historical variation
- **Example:** `0.82` = change magnitude is at 82nd percentile of historical flood variations

### Metrics Fields (Examples)

| Metric | Type | Unit | Notes |
|--------|------|------|-------|
| `flood_extent_change_sqkm` | float | km² | Absolute area increase/decrease |
| `flood_extent_change_percent` | float | % | Relative change from before extent |
| `max_water_depth_m` | float | m | Maximum water depth observed during window |
| `affected_pixels` | integer | — | Number of grid cells where flood state changed |
| `water_surface_elevation_m` | float | m | Water surface elevation above datum |

### Spatial Context Fields (Examples)

| Field | Type | Description |
|-------|------|-------------|
| `location` | string | Geographic description (e.g., "River Valley, downstream reach") |
| `elevation_range_m` | string | Range notation (e.g., "45–78") |
| `land_cover` | array[string] | Land cover types (e.g., ["grassland", "urban"]) |
| `proximity_to_asset_km` | float | Distance to nearest asset |

### Hydrology Fields (Examples)

| Field | Type | Description |
|-------|------|-------------|
| `rainfall_mm_72h` | float | Cumulative rainfall in 72h prior to observation |
| `discharge_percentile` | float | River discharge as percentile of historical record (0–100) |
| `antecedent_soil_moisture` | string | Qualitative soil moisture state (e.g., "high", "normal", "low") |

### Example Payload

```json
{
  "finding_type": "flood_change_detection",
  "event_id": "FLOOD-EVENT-2025-0042",
  "observation_window": {
    "before": "2025-03-10T00:00:00Z",
    "after": "2025-03-15T00:00:00Z"
  },
  "severity_raw": {
    "value": 0.82,
    "percentile": 88,
    "unit_description": "flood extent change relative to historical variation"
  },
  "metrics": {
    "flood_extent_change_sqkm": 12.3,
    "flood_extent_change_percent": 8.2,
    "max_water_depth_m": 2.1,
    "affected_pixels": 15678,
    "water_surface_elevation_m": 125.4
  },
  "spatial_context": {
    "location": "River Valley, downstream reach",
    "elevation_range_m": "45–78",
    "land_cover": ["grassland", "urban"],
    "proximity_to_asset_km": 1.2
  },
  "hydrology": {
    "rainfall_mm_72h": 145,
    "discharge_percentile": 92,
    "antecedent_soil_moisture": "high"
  },
  "timestamp": "2025-03-15T08:00:00Z"
}
```

---

## Finding Type: `temperature_spike` / `vegetation_anomaly`

### Purpose

Spatial or temporal anomaly detected in sensor data or analytical output (extensible for other anomaly types).

### Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `finding_type` | string | ✓ | `"temperature_spike"`, `"vegetation_anomaly"`, etc. |
| `anomaly_id` | string | ✗ | Unique anomaly identifier (e.g., `"ANOMALY-2025-00891"`) |
| `severity_raw` | SeverityRaw | ✓ | Observable deviation magnitude (0.0–1.0 normalized) |
| `baseline` | object | ✓ | Historical baseline statistics (mean, std_dev, period) |
| `observed` | object | ✓ | Current observation (peak value, duration, timestamp) |
| `deviation` | object | ✓ | Magnitude measures (std_devs, percent change) |
| `spatial_context` | object | ✗ | Sensor location and nearby features |
| `temporal_context` | object | ✗ | Environmental factors (wind, clouds, sun angle) |
| `note` | string | ✗ | Additional context or correlation notes |
| `timestamp` | ISO 8601 | ✗ | When this finding was generated |

### Severity_raw Interpretation

- **Value:** Normalized 0.0–1.0 representing deviation magnitude
- **Example:** `0.76` = anomaly magnitude is at 76th percentile of historical deviations

### Baseline Fields (Examples)

| Field | Type | Description |
|-------|------|-------------|
| `mean_celsius` | float | Historical mean (for temperature) |
| `std_dev` | float | Historical standard deviation |
| `observation_period_days` | integer | Days of history used for baseline |
| `mean_ndvi` | float | Historical mean vegetation index (for NDVI anomalies) |

### Observed Fields (Examples)

| Field | Type | Description |
|-------|------|-------------|
| `peak_celsius` | float | Peak temperature during anomaly event |
| `duration_hours` | float | How long the anomaly lasted |
| `timestamp` | ISO 8601 | When the anomaly was observed |
| `peak_ndvi` | float | Peak vegetation index value |

### Deviation Fields (Examples)

| Field | Type | Description |
|-------|------|-------------|
| `magnitude_std_devs` | float | Deviation expressed in standard deviations (e.g., 5.6 σ) |
| `change_from_baseline_percent` | float | Percentage change from baseline mean |

### Spatial Context Fields (Examples)

| Field | Type | Description |
|-------|------|-------------|
| `location` | string | Descriptive location (e.g., "Sensor Node #042, Urban District 3") |
| `nearby_features` | array[string] | Proximal features (e.g., ["paved surface 50m south", "vegetation 120m north"]) |
| `elevation_m` | float | Sensor elevation above datum |
| `sensor_id` | string | Hardware identifier |

### Temporal Context Fields (Examples)

| Field | Type | Description |
|-------|------|-------------|
| `wind_speed_mps` | float | Wind speed in m/s at time of anomaly |
| `cloud_cover_percent` | float | Cloud cover 0–100% |
| `sun_angle_degrees` | float | Solar elevation angle |
| `time_of_day` | string | Hour of day (e.g., "14:00") |

### Example Payload (Temperature Spike)

```json
{
  "finding_type": "temperature_spike",
  "anomaly_id": "ANOMALY-2025-00891",
  "severity_raw": {
    "value": 0.76,
    "percentile": 92,
    "unit_description": "temperature deviation as fraction of historical variation"
  },
  "baseline": {
    "mean_celsius": 18.5,
    "std_dev": 2.1,
    "observation_period_days": 30
  },
  "observed": {
    "peak_celsius": 30.2,
    "duration_hours": 4,
    "timestamp": "2025-03-15T14:00:00Z"
  },
  "deviation": {
    "magnitude_std_devs": 5.6,
    "change_from_baseline_percent": 63.2
  },
  "spatial_context": {
    "location": "Sensor Node #042, Urban District 3",
    "nearby_features": ["paved surface 50m south", "vegetation 120m north"],
    "elevation_m": 45,
    "sensor_id": "SENSOR-042-TEMP"
  },
  "temporal_context": {
    "wind_speed_mps": 1.2,
    "cloud_cover_percent": 5,
    "sun_angle_degrees": 68
  },
  "note": "Anomaly correlates with loss of cloud cover and low wind—classic urban heat island signature.",
  "timestamp": "2025-03-15T14:30:00Z"
}
```

---

## Validation & Routing

### 1. Finding Type Validation

GeoAI modules MUST emit findings with `finding_type` matching one of:
- `flood_proximity`
- `flood_change_detection`
- `temperature_spike` (or other anomaly types defined in future)
- `vegetation_anomaly`

Unrecognized `finding_type` → API returns **400 Bad Request**.

### 2. Template Routing

| Finding Type | Template | Explanation Purpose |
|--------------|----------|---------------------|
| `flood_proximity` | `asset_risk.txt` | Why is this asset flagged for flood risk? |
| `flood_change_detection` | `flood_explanation.txt` | What changed in flood extent/depth, and why? |
| `temperature_spike`, `vegetation_anomaly` | `anomaly_summary.txt` | What is this anomaly and why did it occur? |

### 3. Schema Validation

All payloads are validated by Pydantic models in `api/schemas/payloads.py`:
- `FloodProximityFinding`
- `FloodChangeFinding`
- `AnomalyFinding`

Invalid payloads → API returns **422 Unprocessable Entity** with field-level error details.

---

## Integration: GeoAI → Reasoning

### Workflow

1. **GeoAI Module Emits Finding**
   - Runs deterministic spatial analysis (proximity, change detection, anomaly)
   - Constructs payload matching one of the schemas above
   - Validates payload locally (optional, recommended)

2. **Client Calls `/explain` Endpoint**
   ```bash
   POST /explain
   Content-Type: application/json
   
   {
     "subject": "ASSET-12345",
     "template": "asset_risk",
     "context": <GeoAI finding payload>
   }
   ```

3. **API Validates & Routes**
   - Pydantic validates context against schema
   - Logs request with subject, finding_type, severity_raw
   - Renders context as indented JSON
   - Passes to reasoning_service.explain()

4. **Reasoning Service Explains**
   - Loads template (asset_risk.txt, etc.)
   - Interpolates {subject} and {context}
   - Calls Ollama with LLaMA 3.3
   - Returns plain-language explanation

5. **API Returns Response**
   ```json
   {
     "subject": "ASSET-12345",
     "template": "asset_risk",
     "explanation": "Asset ASSET-12345 is 2.5 km from an active flood zone...",
     "model": "llama3.3"
   }
   ```

---

## Error Handling

| Scenario | HTTP Status | Error Type | Guidance |
|----------|-------------|-----------|----------|
| Invalid finding_type | 400 | Unknown template (if finding_type maps to unsupported template) | Ensure finding_type matches supported list |
| Missing required field | 422 | Validation error | Check schema definition above for required fields |
| Invalid metric value | 422 | Validation error | Metrics should be numeric; severity_raw 0.0–1.0 |
| Ollama unreachable | 503 | Ollama unavailable | Check Ollama service health |
| Malformed JSON | 400 | JSON decode error | Ensure valid JSON syntax |

---

## Future Extensions

### New Anomaly Types

To add support for a new anomaly (e.g., `drainage_blockage`):

1. Update `FindingType` literal in `api/schemas/payloads.py`
2. Add new schema class (e.g., `DrainageBlockageFinding`)
3. Update `GeoAIFinding` union type
4. Add template to `reasoning/prompt_templates/`
5. Update this contract document

### New Finding Types

To add entirely new finding types (e.g., `soil_subsidence`):
- Follow same process as "New Anomaly Types"
- Ensure template + schema are in sync
- Document metrics and context structure

---

## Checklist for GeoAI Module Implementation

- [ ] Finding payload matches one schema in this document
- [ ] All required fields populated
- [ ] Metrics use raw values (not scores or indices)
- [ ] Geometry in WKT or GeoJSON format (if included)
- [ ] Timestamp in ISO 8601 format
- [ ] Severity_raw normalized to 0.0–1.0
- [ ] Signals/notes use observational language (no prediction)
- [ ] Payload validated before transmission
- [ ] Error responses logged with full payload for debugging

---

## References

- **Pydantic Schemas:** `api/schemas/payloads.py`
- **Context Examples:** `reasoning/prompt_templates/GEOAI_CONTEXT_GUIDE.md`
- **Reasoning Templates:** `reasoning/prompt_templates/*.txt`
- **API Spec:** `api/API_SPEC.md`
- **Steps 1–3 Summary:** `STEPS_1_3_COMPLETION.md`
