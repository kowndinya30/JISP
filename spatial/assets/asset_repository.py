"""Asset repository contract — shape only; no DB logic yet.

Implementations will talk to PostgreSQL + PostGIS in a later step.
This module MUST NOT import from ingestion, geoai, timeseries,
reasoning, api, or ui.
"""

from __future__ import annotations

from typing import Iterable, Protocol

from spatial.assets.asset_model import Asset


class AssetRepository(Protocol):
    """Contract for asset persistence and spatial lookup."""

    def get(self, asset_id: str) -> Asset | None:
        """Return the asset with the given id, or None if missing."""
        ...

    def upsert(self, asset: Asset) -> None:
        """Insert or update an asset by id."""
        ...

    def within_bbox(
        self,
        minx: float,
        miny: float,
        maxx: float,
        maxy: float,
    ) -> Iterable[Asset]:
        """Yield assets intersecting the axis-aligned bounding box."""
        ...
