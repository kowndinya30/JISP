"""ANZ / BoM (Bureau of Meteorology) ingestor — shape only; logic TBD."""

from __future__ import annotations

from typing import Any

from ingestion.base_ingestor import BaseIngestor


class BoMIngestor(BaseIngestor):
    """Ingestor for Australia's Bureau of Meteorology data."""

    source = "anz-bom"

    def fetch(self) -> Any:
        raise NotImplementedError

    def normalize(self, raw: Any) -> list[dict[str, Any]]:
        raise NotImplementedError
