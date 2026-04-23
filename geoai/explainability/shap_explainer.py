"""SHAP attribution — signatures only; logic TBD.

Produces feature-level attribution for a trained model. The narrative
explanation layer (`reasoning/`) consumes attribution indirectly via
the API's Pattern-A composition — never by importing this module.
"""

from __future__ import annotations

from typing import Any


def attribute(model: Any, features: dict[str, Any]) -> dict[str, float]:
    """Compute per-feature SHAP attribution. Logic TBD."""
    raise NotImplementedError
