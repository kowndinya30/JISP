"""Clustering models — signatures only; logic TBD.

Will use HDBSCAN / DBSCAN per the approved stack.
"""

from __future__ import annotations

from typing import Any


def cluster(features: list[dict[str, Any]]) -> list[int]:
    """Cluster feature rows; return one cluster label per row. TBD."""
    raise NotImplementedError
