"""Temporal feature extraction — signatures only; logic TBD."""

from __future__ import annotations

from datetime import datetime
from typing import Any


def compute_temporal_features(
    asset_id: str,
    start: datetime,
    end: datetime,
) -> dict[str, Any]:
    """Compute temporal features for an asset over a time window. TBD."""
    raise NotImplementedError
