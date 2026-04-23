"""Time-series domain model — shape only.

Responsibility (strict): TimescaleDB time-series ONLY. No spatial, no
ingestion, no AI, no reasoning, no API concerns.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Observation:
    """A time-stamped measurement linked to an asset.

    Attributes:
        asset_id: The asset this observation belongs to.
        metric: Canonical metric name (e.g. ``"rainfall_mm"``,
            ``"river_stage_m"``, ``"soil_moisture_pct"``). Units live
            in the metric name.
        value: Numeric value.
        observed_at: UTC timestamp of the measurement.
    """

    asset_id: str
    metric: str
    value: float
    observed_at: datetime
