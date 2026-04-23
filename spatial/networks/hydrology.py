"""Hydrology network model — signatures only; logic TBD."""

from __future__ import annotations

from spatial.assets.asset_model import Asset


def upstream_catchment(asset: Asset) -> list[Asset]:
    """Return the set of assets upstream of the given asset. TBD."""
    raise NotImplementedError
