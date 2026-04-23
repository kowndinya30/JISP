"""Time-series queries — signatures only."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

from timeseries.models import Observation


def range_for_asset(
    asset_id: str,
    metric: str,
    start: datetime,
    end: datetime,
) -> Iterable[Observation]:
    """Fetch observations for (asset, metric) between start and end. TBD."""
    raise NotImplementedError


def latest_for_asset(asset_id: str, metric: str) -> Observation | None:
    """Fetch the most recent observation for (asset, metric). TBD."""
    raise NotImplementedError
