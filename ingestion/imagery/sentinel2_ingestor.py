"""Sentinel-2 imagery ingestor — shape only; logic TBD."""

from __future__ import annotations

from typing import Any

from ingestion.base_ingestor import BaseIngestor


class Sentinel2Ingestor(BaseIngestor):
    """Ingestor for Sentinel-2 satellite imagery."""

    source = "imagery-sentinel2"

    def fetch(self) -> Any:
        raise NotImplementedError

    def normalize(self, raw: Any) -> list[dict[str, Any]]:
        raise NotImplementedError
