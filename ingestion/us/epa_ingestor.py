"""US / EPA ingestor — shape only; logic TBD."""

from __future__ import annotations

from typing import Any

from ingestion.base_ingestor import BaseIngestor


class EPAIngestor(BaseIngestor):
    """Ingestor for United States Environmental Protection Agency data."""

    source = "us-epa"

    def fetch(self) -> Any:
        raise NotImplementedError

    def normalize(self, raw: Any) -> list[dict[str, Any]]:
        raise NotImplementedError
