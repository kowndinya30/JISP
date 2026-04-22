"""Pydantic payload schemas for the JISP API."""

from typing import Any, Literal

from pydantic import BaseModel, Field


TemplateName = Literal["asset_risk", "flood_explanation", "anomaly_summary"]


class ExplainRequest(BaseModel):
    subject: str = Field(
        ...,
        description="What to explain (e.g. asset id, inspection id, event id).",
    )
    template: TemplateName = Field(
        default="asset_risk",
        description="Which reasoning prompt template to use.",
    )
    context: dict[str, Any] | None = Field(
        default=None,
        description="Optional structured context passed to the reasoning layer.",
    )


class ExplainResponse(BaseModel):
    subject: str
    template: TemplateName
    explanation: str
    model: str | None = None
