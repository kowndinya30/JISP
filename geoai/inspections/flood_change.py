"""Flood-change inspection — shape only; logic lands in a later step.

Pattern-A composition: `detect(...)` returns a `FloodChangeDetection`
the API layer can feed straight into `reasoning_service.explain(...)`.
No imports from `reasoning/`, `api/`, `ui/`, or sibling core folders.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from geoai import TemplateName


@dataclass(frozen=True)
class FloodChangeDetection:
    """Outcome of a single flood-change detection run.

    Attributes:
        subject: Asset identifier the detection applies to.
        context: Structured signals (rainfall, water-extent change,
            dates, confidence) suitable for the reasoning layer.
        template: Which reasoning template the API should use
            (default: ``"flood_explanation"``).
    """

    subject: str
    context: dict[str, Any] = field(default_factory=dict)
    template: TemplateName = "flood_explanation"


def detect(asset_id: str) -> FloodChangeDetection:
    """Run flood-change detection against a single asset.

    Logic deferred to a later step. Signature kept narrow on purpose;
    date ranges, raster paths, and thresholds will be added alongside
    the real implementation.
    """
    raise NotImplementedError
