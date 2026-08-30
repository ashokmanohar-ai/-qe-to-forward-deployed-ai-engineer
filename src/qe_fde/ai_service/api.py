"""FastAPI delivery layer for the provider-neutral reference service."""

from __future__ import annotations

import hashlib
import secrets
import uuid
from collections.abc import Awaitable, Callable
from dataclasses import asdict

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, ConfigDict, Field
from starlette.responses import Response

from qe_fde import __version__
from qe_fde.ai_service.agent import (
    AgentWorkflow,
    ExecutionContext,
    ToolCall,
    ToolError,
    ToolRegistry,
    ToolSpec,
)
from qe_fde.ai_service.config import Settings
from qe_fde.ai_service.evaluation import EvaluationCase, EvaluationRunner
from qe_fde.ai_service.observability import Observability
from qe_fde.ai_service.retrieval import (
    Document,
    InMemoryVectorStore,
    RAGAssistant,
    RetrievalError,
)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class DocumentInput(StrictModel):
    document_id: str = Field(min_length=1, max_length=128)
    tenant_id: str = Field(min_length=1, max_length=128)
    source: str = Field(min_length=1, max_length=256)
    version: str = Field(min_length=1, max_length=64)
    text: str = Field(min_length=1, max_length=100_000)
    metadata: dict[str, str] = Field(default_factory=dict)


class AskInput(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=128)
    question: str = Field(min_length=1, max_length=2_000)
    top_k: int = Field(default=3, ge=1, le=20)


class ToolCallInput(StrictModel):
    name: str = Field(min_length=1, max_length=64)
    arguments: dict[str, object] = Field(default_factory=dict)


class AgentInput(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=128)
    user_id: str = Field(min_length=1, max_length=128)
    calls: list[ToolCallInput] = Field(min_length=1, max_length=10)
    approved_tools: list[str] = Field(default_factory=list, max_length=10)
    idempotency_key: str | None = Field(default=None, min_length=8, max_length=128)


class EvaluationCaseInput(StrictModel):
    case_id: str = Field(min_length=1, max_length=128)
    tenant_id: str = Field(min_length=1, max_length=128)
    question: str = Field(min_length=1, max_length=2_000)
    expected_terms: list[str] = Field(default_factory=list, max_length=50)
    forbidden_terms: list[str] = Field(default_factory=list, max_length=50)
    minimum_citations: int = Field(default=1, ge=0, le=20)
    segment: str = Field(default="default", min_length=1, max_length=128)
    critical: bool = False


class EvaluationInput(StrictModel):
    cases: list[EvaluationCaseInput] = Field(min_length=1, max_length=500)
    case_threshold: float = Field(default=0.8, ge=0, le=1)
    release_pass_rate: float = Field(default=0.9, ge=0, le=1)


def _require_string(arguments: dict[str, object], name: str, *, max_length: int = 500) -> str:
    value = arguments.get(name)
    if not isinstance(value, str) or not value.strip() or len(value) > max_length:
        raise ToolError(f"argument {name!r} must be a non-empty string")
    return value.strip()


def _build_workflow(max_steps: int) -> AgentWorkflow:
    registry = ToolRegistry()

    def lookup_order(arguments: dict[str, object], context: ExecutionContext) -> dict[str, object]:
        order_id = _require_string(arguments, "order_id", max_length=64)
        synthetic_orders: dict[tuple[str, str], dict[str, object]] = {
            ("demo", "ORD-1001"): {
                "order_id": "ORD-1001",
                "status": "delayed",
                "eta_days": 3,
            }
        }
        return synthetic_orders.get(
            (context.tenant_id, order_id),
            {"order_id": order_id, "status": "not_found"},
        )

    def create_case(arguments: dict[str, object], context: ExecutionContext) -> dict[str, object]:
        subject = _require_string(arguments, "subject", max_length=200)
        digest_input = f"{context.tenant_id}:{context.idempotency_key}:{subject}"
        case_id = "CASE-" + hashlib.sha256(digest_input.encode("utf-8")).hexdigest()[:10]
        return {"case_id": case_id, "status": "created", "subject": subject}

    registry.register(
        ToolSpec(
            name="lookup_order",
            description="Read a synthetic order that belongs to the authenticated tenant.",
            handler=lookup_order,
        )
    )
    registry.register(
        ToolSpec(
            name="create_case",
            description="Create a synthetic support case after explicit confirmation.",
            handler=create_case,
            read_only=False,
            requires_confirmation=True,
        )
    )
    return AgentWorkflow(registry, max_steps=max_steps)


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved = settings or Settings.from_env()
    store = InMemoryVectorStore(max_documents=resolved.max_documents)
    assistant = RAGAssistant(store)
    workflow = _build_workflow(resolved.max_tool_steps)
    evaluations = EvaluationRunner(assistant)
    telemetry = Observability()

    app = FastAPI(
        title="QE to FDE AI Reference Service",
        version=__version__,
        description=(
            "A provider-neutral learning service demonstrating tenant-scoped retrieval, "
            "citations, bounded tools, evaluation, authentication, metrics, and traces."
        ),
    )
    app.state.store = store
    app.state.telemetry = telemetry

    def require_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> str:
        if x_api_key is None or not secrets.compare_digest(x_api_key, resolved.api_key):
            telemetry.increment("fde_auth_failures_total")
            raise HTTPException(status_code=401, detail={"code": "UNAUTHORIZED"})
        return x_api_key

    @app.middleware("http")
    async def correlation_middleware(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        trace_id = request.headers.get("X-Correlation-ID") or uuid.uuid4().hex
        request.state.trace_id = trace_id
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = trace_id
        return response

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "healthy", "service": "qe-fde-ai", "version": __version__}

    @app.get("/v1/status", dependencies=[Depends(require_api_key)])
    def status() -> dict[str, object]:
        return {
            "status": "ready",
            "environment": resolved.environment,
            "document_count": store.count(),
            "tools": workflow.registry.names(),
        }

    @app.post("/v1/documents", status_code=201, dependencies=[Depends(require_api_key)])
    def ingest(payload: DocumentInput, request: Request) -> dict[str, object]:
        try:
            with telemetry.span(request.state.trace_id, "ingest", tenant_id=payload.tenant_id):
                store.upsert(
                    Document(
                        document_id=payload.document_id,
                        tenant_id=payload.tenant_id,
                        source=payload.source,
                        version=payload.version,
                        text=payload.text,
                        metadata=payload.metadata,
                    )
                )
            telemetry.increment("fde_ingestion_total", status="accepted")
            return {"status": "accepted", "document_id": payload.document_id}
        except RetrievalError as exc:
            telemetry.increment("fde_ingestion_total", status="rejected")
            raise HTTPException(status_code=400, detail={"code": "INVALID_DOCUMENT"}) from exc

    @app.post("/v1/ask", dependencies=[Depends(require_api_key)])
    def ask(payload: AskInput, request: Request) -> dict[str, object]:
        try:
            with telemetry.span(request.state.trace_id, "rag", tenant_id=payload.tenant_id):
                answer = assistant.ask(
                    payload.question, tenant_id=payload.tenant_id, top_k=payload.top_k
                )
            telemetry.increment("fde_answers_total", abstained=str(answer.abstained).lower())
            return {**asdict(answer), "trace_id": request.state.trace_id}
        except RetrievalError as exc:
            raise HTTPException(status_code=400, detail={"code": "INVALID_QUERY"}) from exc

    @app.post("/v1/agent/run", dependencies=[Depends(require_api_key)])
    def run_agent(payload: AgentInput, request: Request) -> dict[str, object]:
        context = ExecutionContext(
            tenant_id=payload.tenant_id,
            user_id=payload.user_id,
            approved_tools=frozenset(payload.approved_tools),
            idempotency_key=payload.idempotency_key,
        )
        calls = [ToolCall(name=call.name, arguments=call.arguments) for call in payload.calls]
        try:
            with telemetry.span(request.state.trace_id, "agent", tenant_id=payload.tenant_id):
                results = workflow.run(calls, context)
            telemetry.increment("fde_agent_runs_total", status="success")
            return {
                "results": [asdict(result) for result in results],
                "trace_id": request.state.trace_id,
            }
        except ToolError as exc:
            telemetry.increment("fde_agent_runs_total", status="denied")
            raise HTTPException(
                status_code=400,
                detail={"code": "TOOL_REQUEST_DENIED", "message": str(exc)},
            ) from exc

    @app.post("/v1/evaluations/run", dependencies=[Depends(require_api_key)])
    def run_evaluation(payload: EvaluationInput, request: Request) -> dict[str, object]:
        cases = [
            EvaluationCase(
                case_id=case.case_id,
                tenant_id=case.tenant_id,
                question=case.question,
                expected_terms=tuple(case.expected_terms),
                forbidden_terms=tuple(case.forbidden_terms),
                minimum_citations=case.minimum_citations,
                segment=case.segment,
                critical=case.critical,
            )
            for case in payload.cases
        ]
        with telemetry.span(request.state.trace_id, "evaluation"):
            report = evaluations.run(
                cases,
                case_threshold=payload.case_threshold,
                release_pass_rate=payload.release_pass_rate,
            )
        telemetry.increment("fde_evaluation_runs_total", passed=str(report.passed).lower())
        return {**asdict(report), "trace_id": request.state.trace_id}

    @app.get(
        "/metrics",
        response_class=PlainTextResponse,
        dependencies=[Depends(require_api_key)],
    )
    def metrics() -> str:
        return telemetry.prometheus()

    return app
