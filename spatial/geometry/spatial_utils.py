"""Spatial geometry utilities — signatures only; logic TBD."""

from __future__ import annotations


def buffer_meters(geometry_wkt: str, meters: float) -> str:
    """Return a buffered geometry as WKT. Logic TBD."""
    raise NotImplementedError


def distance_meters(a_wkt: str, b_wkt: str) -> float:
    """Return geodesic distance between two geometries in meters. TBD."""
    raise NotImplementedError
