"""Erosion-detection inspection — shape only; logic lands in a later step.

Pattern-A composition: `detect(...)` returns an `ErosionDetection` the
API layer feeds into `reasoning_service.explain(...)`. No cross-folder
imports.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from geoai import TemplateName


@dataclass(frozen=True)
class ErosionDetection:
    """Outcome of a single erosion-detection run.

    Attributes:
        subject: Asset identifier the detection applies to.
        context: Structured signals (slope, soil type, land-cover
            change, proximity signals) for the reasoning layer.
        template: Which reasoning template the API should use
            (default: ``"asset_risk"``).
    """

    subject: str
    context: dict[str, Any] = field(default_factory=dict)
    template: TemplateName = "asset_risk"


def detect(asset_id: str) -> ErosionDetection:
    """Run erosion detection against a single asset. Logic TBD."""
    raise NotImplementedError
