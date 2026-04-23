"""US / USGS ingestor — shape only; logic TBD."""

from __future__ import annotations

from typing import Any

from ingestion.base_ingestor import BaseIngestor


class USGSIngestor(BaseIngestor):
    """Ingestor for United States Geological Survey data."""

    source = "us-usgs"

    def fetch(self) -> Any:
        raise NotImplementedError

    def normalize(self, raw: Any) -> list[dict[str, Any]]:
        raise NotImplementedError
