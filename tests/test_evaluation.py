from qe_fde.ai_service.evaluation import EvaluationCase, EvaluationRunner
from qe_fde.ai_service.retrieval import Document, InMemoryVectorStore, RAGAssistant


def test_critical_segment_failure_blocks_release() -> None:
    store = InMemoryVectorStore()
    store.upsert(
        Document(
            document_id="doc-1",
            tenant_id="demo",
            source="manual",
            version="1",
            text="Password reset links expire after fifteen minutes.",
        )
    )
    runner = EvaluationRunner(RAGAssistant(store))
    cases = [
        EvaluationCase(
            case_id="good",
            tenant_id="demo",
            question="When does a password reset link expire?",
            expected_terms=("fifteen minutes",),
            segment="common",
        ),
        EvaluationCase(
            case_id="critical",
            tenant_id="demo",
            question="What emergency bypass is allowed?",
            expected_terms=("no bypass",),
            minimum_citations=0,
            segment="high-risk",
            critical=True,
        ),
    ]

    report = runner.run(cases, release_pass_rate=0.5)

    assert report.pass_rate == 0.5
    assert not report.passed
    assert report.segment_pass_rates["high-risk"] == 0.0
