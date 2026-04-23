"""Time-series ingestion helpers — signatures only.

Bridges normalized records into TimescaleDB. The normalization itself
lives in `ingestion/`; this module only persists what it is given.
"""

from __future__ import annotations

from typing import Iterable

from timeseries.models import Observation


def persist(observations: Iterable[Observation]) -> int:
    """Persist observations to TimescaleDB. Return the count written. TBD."""
    raise NotImplementedError
