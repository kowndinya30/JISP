"""Reasoning routes.

Step 2: exposes `/explain` as a stub. Step 3 will replace the stub body
with a call into `reasoning.reasoning_service` (Ollama + Kimi). No
prediction or scoring — explanation only.
"""

from fastapi import APIRouter

from api.schemas.payloads import ExplainRequest, ExplainResponse

router = APIRouter(tags=["reasoning"])


@router.post("/explain", response_model=ExplainResponse)
def explain(request: ExplainRequest) -> ExplainResponse:
    return ExplainResponse(
        subject=request.subject,
        explanation=(
            "Reasoning service is not wired yet (Step 2 stub). "
            "Ollama + Kimi integration lands in Step 3."
        ),
        model=None,
    )
