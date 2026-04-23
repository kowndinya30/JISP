"""Reasoning routes: explainability endpoint for GeoAI findings.

This module exposes the POST /explain endpoint, which transforms GeoAI
findings into plain-language explanations using LLaMA 3.3 via Ollama.

CRITICAL CONSTRAINT: This endpoint does NOT predict, score, or recommend.
It only explains observed signals in the GeoAI context.

Endpoint:
    POST /explain — Explain a GeoAI finding using a template.

Error Mapping:
    - UnknownTemplateError → 400 Bad Request
    - OllamaUnavailableError → 503 Service Unavailable

Audit Trail:
    All requests and responses are logged (see logging.yaml).

Request/Response Contracts:
    See api/schemas/payloads.py (ExplainRequest, ExplainResponse).

Expected Context by Template:
    See reasoning/prompt_templates/GEOAI_CONTEXT_GUIDE.md.
"""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, status

from api.schemas.payloads import ExplainRequest, ExplainResponse
from reasoning.ollama_client import OllamaUnavailableError
from reasoning.reasoning_service import UnknownTemplateError, explain as run_explain


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="",
    tags=["reasoning"],
    responses={
        400: {"description": "Unknown template or invalid request"},
        503: {"description": "Ollama unavailable"},
    },
)


@router.post(
    "/explain",
    response_model=ExplainResponse,
    summary="Explain a GeoAI finding",
    description=(
        "Generate a plain-language explanation of a GeoAI finding using LLaMA 3.3. "
        "Explanation is observational only: no prediction, scoring, or recommendations. "
        "See reasoning/prompt_templates/GEOAI_CONTEXT_GUIDE.md for expected context structures."
    ),
)
def explain(request: ExplainRequest) -> ExplainResponse:
    """Orchestrate the reasoning service to explain a GeoAI finding.

    Args:
        request: ExplainRequest with subject, template, and optional context.

    Returns:
        ExplainResponse with the narrative explanation and model metadata.

    Raises:
        HTTPException(400): Unknown template.
        HTTPException(503): Ollama unreachable.

    Logging:
        All requests and responses are logged with subject, template, and
        result status for audit and debugging purposes.
    """
    logger.info(
        "Explain request received",
        extra={
            "subject": request.subject,
            "template": request.template,
            "context_keys": (
                list(request.context.keys()) if request.context else None
            ),
        },
    )

    try:
        result = run_explain(
            subject=request.subject,
            template=request.template,
            context=request.context,
        )
    except UnknownTemplateError as e:
        logger.warning(
            "Unknown template error",
            extra={"subject": request.subject, "template": request.template},
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except OllamaUnavailableError as e:
        logger.error(
            "Ollama unavailable",
            extra={"subject": request.subject, "template": request.template},
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        ) from e

    response = ExplainResponse(
        subject=result.subject,
        template=result.template,
        explanation=result.explanation,
        model=result.model,
    )

    logger.info(
        "Explain request completed",
        extra={
            "subject": request.subject,
            "template": request.template,
            "model": result.model,
            "explanation_length": len(result.explanation),
        },
    )

    return response
