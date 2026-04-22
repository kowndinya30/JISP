"""Reasoning routes.

Exposes `POST /explain`, wired to `reasoning.reasoning_service`, which
uses Ollama + Llama 3.3. No prediction or scoring — explanation only.

Error mapping:
- Unknown template → 400 Bad Request
- Ollama unreachable / non-JSON / non-2xx → 503 Service Unavailable
"""

from fastapi import APIRouter, HTTPException, status

from api.schemas.payloads import ExplainRequest, ExplainResponse
from reasoning.ollama_client import OllamaUnavailableError
from reasoning.reasoning_service import UnknownTemplateError, explain as run_explain


router = APIRouter(tags=["reasoning"])


@router.post("/explain", response_model=ExplainResponse)
def explain(request: ExplainRequest) -> ExplainResponse:
    try:
        result = run_explain(
            subject=request.subject,
            template=request.template,
            context=request.context,
        )
    except UnknownTemplateError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except OllamaUnavailableError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        ) from e

    return ExplainResponse(
        subject=result.subject,
        template=result.template,
        explanation=result.explanation,
        model=result.model,
    )
