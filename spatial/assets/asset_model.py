"""Asset domain model — shape only; persistence logic lives elsewhere.

Responsibility (strict): PostGIS, assets, geometry ONLY. No ingestion,
no AI, no reasoning, no API concerns.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Asset:
    """A geospatially-located object JISP reasons about.

    Attributes:
        id: Canonical asset identifier (stable across ingestion runs).
        type: Domain-specific asset type (e.g. ``"pipe"``, ``"bridge"``).
        geometry_wkt: Well-Known Text geometry. PostGIS handles the
            spatial-reference projection at the storage layer.
        attributes: Arbitrary source attributes (flatly serializable).
    """

    id: str
    type: str
    geometry_wkt: str
    attributes: dict[str, Any] = field(default_factory=dict)
