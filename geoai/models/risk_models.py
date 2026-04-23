"""Risk models — signatures only; logic TBD.

Returns structured risk signals (features + attribution) that an
inspection's `*Detection` dataclass carries in its `context`. The API
layer later composes these with `reasoning_service.explain(...)` —
this module does NOT import reasoning / api / ui / sibling core
folders.
"""

from __future__ import annotations

from typing import Any


def score_asset(asset_id: str, features: dict[str, Any]) -> dict[str, Any]:
    """Produce a structured risk signal for an asset. Logic TBD.

    Intended return shape: a dict containing contributing feature
    values, simple descriptive statistics, and (optionally) a scalar
    indicator. The exact schema is deferred until the real model lands.
    """
    raise NotImplementedError
