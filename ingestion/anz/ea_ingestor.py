"""ANZ / EA (Environment Agency) ingestor — shape only; logic TBD."""

from __future__ import annotations

from typing import Any

from ingestion.base_ingestor import BaseIngestor


class EAIngestor(BaseIngestor):
    """Ingestor for the Environment Agency (ANZ) data."""

    source = "anz-ea"

    def fetch(self) -> Any:
        raise NotImplementedError

    def normalize(self, raw: Any) -> list[dict[str, Any]]:
        raise NotImplementedError
