"""Pydantic payload schemas for the JISP API."""

from typing import Any

from pydantic import BaseModel, Field


class ExplainRequest(BaseModel):
    subject: str = Field(
        ...,
        description="What to explain (e.g. asset id, inspection id, event id).",
    )
    context: dict[str, Any] | None = Field(
        default=None,
        description="Optional structured context passed to the reasoning layer.",
    )


class ExplainResponse(BaseModel):
    subject: str
    explanation: str
    model: str | None = None
