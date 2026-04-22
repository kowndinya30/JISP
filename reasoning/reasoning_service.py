"""Turn pre-field signals into plain-language explanations.

Responsibility (strict): explanation only — no prediction, no scoring.
This module is the single entry point for the `reasoning/` folder and
must not import from `geoai/`, `spatial/`, `timeseries/`, or `api/`.

Flow:
1. Caller picks a template (`asset_risk`, `flood_explanation`,
   `anomaly_summary`) and supplies a subject plus optional context.
2. The template is loaded from `reasoning/prompt_templates/`.
3. Subject + context are interpolated into the template.
4. The rendered prompt is sent to Ollama via `ollama_client.generate`.
5. The trimmed explanation plus the model name are returned.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from reasoning.ollama_client import OllamaConfig, generate


PROMPT_TEMPLATES_DIR = Path(__file__).parent / "prompt_templates"

SUPPORTED_TEMPLATES: tuple[str, ...] = (
    "asset_risk",
    "flood_explanation",
    "anomaly_summary",
)


class UnknownTemplateError(ValueError):
    """Raised when a caller asks for a template that does not exist."""


@dataclass(frozen=True)
class Explanation:
    subject: str
    template: str
    model: str
    explanation: str


def _load_template(name: str) -> str:
    if name not in SUPPORTED_TEMPLATES:
        raise UnknownTemplateError(
            f"Unknown template '{name}'. "
            f"Supported: {', '.join(SUPPORTED_TEMPLATES)}."
        )
    return (PROMPT_TEMPLATES_DIR / f"{name}.txt").read_text(encoding="utf-8")


def _render_context(context: dict[str, Any] | None) -> str:
    if not context:
        return "(none)"
    return json.dumps(context, indent=2, sort_keys=True, default=str)


def explain(
    subject: str,
    template: str,
    context: dict[str, Any] | None = None,
    config: OllamaConfig | None = None,
) -> Explanation:
    """Render `template`, call Ollama, return the narrative explanation."""
    raw_template = _load_template(template)
    prompt = raw_template.format(
        subject=subject,
        context=_render_context(context),
    )
    cfg = config or OllamaConfig.from_env()
    text = generate(prompt, config=cfg).strip()
    return Explanation(
        subject=subject,
        template=template,
        model=cfg.model,
        explanation=text,
    )
