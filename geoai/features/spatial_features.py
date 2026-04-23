"""Spatial feature extraction — signatures only; logic TBD.

Consumers must not import reasoning, api, ui, ingestion, spatial, or
timeseries from this module.
"""

from __future__ import annotations

from typing import Any


def compute_spatial_features(asset_id: str) -> dict[str, Any]:
    """Compute spatial features for a single asset. Logic TBD."""
    raise NotImplementedError
