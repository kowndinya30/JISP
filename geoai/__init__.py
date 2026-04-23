"""JISP GeoAI package.

Responsibility (strict): spatial AI & change detection ONLY.

Pattern-A composition (see ADR 001):
    geoai.*.detect(...) -> *Detection dataclass
                           |
                           v
    api/routes/geoai.py  -> reasoning_service.explain(
                                subject=det.subject,
                                template=det.template,
                                context=det.context,
                            )

GeoAI must NOT import from `reasoning/`, `api/`, `ui/`, `ingestion/`,
`spatial/`, or `timeseries/`. Any cross-folder composition lives in
`api/`, never here.
"""

from typing import Literal


#: Allowed reasoning templates. Mirrors
#: `reasoning.reasoning_service.SUPPORTED_TEMPLATES` — duplicated here
#: so `geoai/` never imports from `reasoning/`.
TemplateName = Literal["asset_risk", "flood_explanation", "anomaly_summary"]
