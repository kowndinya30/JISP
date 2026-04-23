"""Base ingestor contract.

Concrete ingestors under `us/`, `anz/`, and `imagery/` inherit from
`BaseIngestor`. No network I/O, no parsing, no normalization here —
this module defines only the shape. Logic lands in a later step.

Ingestors must NOT import from `spatial/`, `timeseries/`, `geoai/`,
`reasoning/`, `api/`, or `ui/`. Ingestion is strictly one-way:
source -> normalized records.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class IngestionResult:
    """Outcome of a single ingestion run.

    Attributes:
        source: Stable identifier for the source (e.g. ``"us-usgs"``).
        records: Normalized records produced by this run.
    """

    source: str
    records: list[dict[str, Any]]


class BaseIngestor(ABC):
    """Contract for every JISP ingestor.

    Subclasses set `source` and implement `fetch()` + `normalize()`.
    `run()` orchestrates them; its implementation is deferred.
    """

    #: Stable identifier for the source (e.g. ``"us-usgs"``, ``"anz-bom"``).
    source: str

    @abstractmethod
    def fetch(self) -> Any:
        """Pull raw data from the source. No normalization here."""
        raise NotImplementedError

    @abstractmethod
    def normalize(self, raw: Any) -> list[dict[str, Any]]:
        """Transform raw source output into JISP-canonical records."""
        raise NotImplementedError

    def run(self) -> IngestionResult:
        """Fetch + normalize in one call. Logic TBD."""
        raise NotImplementedError
