"""Anomaly-detection inspection — shape only; logic lands in a later step.

Pattern-A composition: `detect(...)` returns an `AnomalyDetection` the
API layer feeds into `reasoning_service.explain(...)`. No cross-folder
imports.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from geoai import TemplateName


@dataclass(frozen=True)
class AnomalyDetection:
    """Outcome of a single anomaly-detection run.

    Attributes:
        subject: Asset identifier the detection applies to.
        context: Structured signals (baseline stats, delta, spatial /
            temporal factors) for the reasoning layer.
        template: Which reasoning template the API should use
            (default: ``"anomaly_summary"``).
    """

    subject: str
    context: dict[str, Any] = field(default_factory=dict)
    template: TemplateName = "anomaly_summary"


def detect(asset_id: str) -> AnomalyDetection:
    """Run anomaly detection against a single asset. Logic TBD."""
    raise NotImplementedError
