# GeoAI Context Guide for Prompt Templates

This document describes the expected structure of GeoAI findings passed as context to reasoning templates. Templates are designed to accept this JSON structure and render clear, factual explanations.

---

## Template: `asset_risk.txt`

**Purpose:** Explain why an asset is flagged based on proximity, sensor signals, or spatial conditions.

**Expected GeoAI Context:**

```json
{
  "asset_id": "ASSET-12345",
  "asset_type": "infrastructure_bridge",
  "finding_type": "flood_proximity",
  "severity_raw": 0.78,
  "metrics": {
    "proximity_km": 2.5,
    "flood_extent_percent": 15,
    "recurrence_interval_years": 100
  },
  "geometry_reference": "POINT(-73.9352 40.7306)",
  "timestamp": "2025-03-15T10:30:00Z",
  "signals": [
    "Active flood zone detected within 5 km",
    "Asset in FEMA floodplain boundary (1% annual chance)",
    "Elevation: 12m above baseline; highest point in zone is 8m"
  ]
}
```

**What the template emphasizes:**
- What signals triggered the flag (without assigning a score)
- Spatial context (proximity, elevation, land type)
- Factors the field team should investigate
- NO predictions of future inundation
- NO risk score or recommendation

---

## Template: `flood_explanation.txt`

**Purpose:** Explain a flood change detection event in spatial and temporal terms.

**Expected GeoAI Context:**

```json
{
  "event_id": "FLOOD-EVENT-2025-0042",
  "finding_type": "flood_change_detection",
  "observation_window": {
    "before": "2025-03-10T00:00:00Z",
    "after": "2025-03-15T00:00:00Z"
  },
  "metrics": {
    "flood_extent_change_sqkm": 12.3,
    "flood_extent_change_percent": 8.2,
    "max_water_depth_m": 2.1,
    "affected_pixels": 15678
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

**What the template emphasizes:**
- What changed and by how much (extent, depth, timing)
- Spatial factors (terrain, land cover, proximity)
- Hydrological drivers (rainfall, discharge) that explain the change
- Investigation points for the field team
- NO predictions of further flooding
- NO severity or risk assignment

---

## Template: `anomaly_summary.txt`

**Purpose:** Explain a spatial or temporal anomaly detected in sensor or analytical data.

**Expected GeoAI Context:**

```json
{
  "anomaly_id": "ANOMALY-2025-00891",
  "finding_type": "temperature_spike",
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
    "elevation_m": 45
  },
  "temporal_context": {
    "wind_speed_mps": 1.2,
    "cloud_cover_percent": 5,
    "sun_angle_degrees": 68
  },
  "note": "Anomaly correlates with loss of cloud cover and low wind"
}
```

**What the template emphasizes:**
- What the anomaly is (deviation magnitude, timing)
- Temporal or spatial context that may explain it
- Environmental factors to investigate
- No severity label or alarm state
- No predictions of future anomalies
- No recommended actions

---

## General Principles

1. **Observational Only:** All context must describe measurements or detections, not predictions.
2. **Metrics Over Scores:** Use raw metrics (extent in km², temperature in °C, percentiles) rather than derived scores.
3. **Explainability:** Include enough supporting detail so the template can explain the "why" without inventing data.
4. **No Downstream Dependencies:** Templates never assume predictive models ran. They only explain GeoAI findings.

---

## Integration Notes

- **GeoAI Module:** When exposing findings via `api/routes/geoai.py`, ensure context matches one of these structures.
- **Reasoning Service:** `reasoning_service.explain()` accepts any JSON context; these are recommendations, not enforced schemas.
- **API Contract:** See `api/schemas/payloads.py` for request/response models.

---

## Example: Full Request/Response

**Request to `POST /explain`:**

```json
{
  "subject": "ASSET-12345",
  "template": "asset_risk",
  "context": {
    "finding_type": "flood_proximity",
    "severity_raw": 0.78,
    "metrics": {
      "proximity_km": 2.5,
      "flood_extent_percent": 15
    },
    "signals": ["Active flood zone detected within 5 km"]
  }
}
```

**Response:**

```json
{
  "subject": "ASSET-12345",
  "template": "asset_risk",
  "explanation": "Asset ASSET-12345 is 2.5 km from an active flood zone with current extent of 15%. The asset sits at elevation 12m in an area where peak water is 8m, providing a 4m buffer. Nearby drainage patterns should be confirmed during field inspection.",
  "model": "llama3.3"
}
```

---

## Future Extensions

As GeoAI modules mature, additional templates may be added:
- `change_point_detection` — Temporal shifts in baseline signals
- `spatial_clustering` — Grouping findings across assets
- `time_series_forecast_context` — Historical vs. current (explanation-only interpretation)

All new templates must follow the same anti-prediction, anti-scoring principles.
