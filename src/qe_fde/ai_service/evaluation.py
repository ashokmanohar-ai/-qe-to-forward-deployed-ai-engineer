"""Small, inspectable evaluation runner and segment-aware release gate."""

from __future__ import annotations

from dataclasses import dataclass

from qe_fde.ai_service.retrieval import Answer, RAGAssistant


@dataclass(frozen=True)
class EvaluationCase:
    case_id: str
    tenant_id: str
    question: str
    expected_terms: tuple[str, ...]
    forbidden_terms: tuple[str, ...] = ()
    minimum_citations: int = 1
    segment: str = "default"
    critical: bool = False


@dataclass(frozen=True)
class EvaluationResult:
    case_id: str
    segment: str
    score: float
    passed: bool
    critical: bool
    citation_count: int
    missing_terms: tuple[str, ...]
    present_forbidden_terms: tuple[str, ...]
    abstained: bool


@dataclass(frozen=True)
class ReleaseReport:
    results: tuple[EvaluationResult, ...]
    passed: bool
    pass_rate: float
    segment_pass_rates: dict[str, float]


def evaluate_answer(
    case: EvaluationCase, answer: Answer, *, threshold: float = 0.8
) -> EvaluationResult:
    normalized = answer.text.casefold()
    missing = tuple(term for term in case.expected_terms if term.casefold() not in normalized)
    forbidden = tuple(term for term in case.forbidden_terms if term.casefold() in normalized)
    expected_count = len(case.expected_terms)
    coverage = 1.0 if expected_count == 0 else (expected_count - len(missing)) / expected_count
    citation_ok = len(answer.citations) >= case.minimum_citations
    score = coverage
    passed = score >= threshold and citation_ok and not forbidden
    return EvaluationResult(
        case_id=case.case_id,
        segment=case.segment,
        score=round(score, 4),
        passed=passed,
        critical=case.critical,
        citation_count=len(answer.citations),
        missing_terms=missing,
        present_forbidden_terms=forbidden,
        abstained=answer.abstained,
    )


class EvaluationRunner:
    def __init__(self, assistant: RAGAssistant) -> None:
        self.assistant = assistant

    def run(
        self,
        cases: list[EvaluationCase],
        *,
        case_threshold: float = 0.8,
        release_pass_rate: float = 0.9,
    ) -> ReleaseReport:
        if not cases:
            raise ValueError("evaluation requires at least one case")
        results = tuple(
            evaluate_answer(
                case,
                self.assistant.ask(case.question, tenant_id=case.tenant_id),
                threshold=case_threshold,
            )
            for case in cases
        )
        pass_rate = sum(result.passed for result in results) / len(results)
        segments: dict[str, list[bool]] = {}
        for result in results:
            segments.setdefault(result.segment, []).append(result.passed)
        segment_rates = {
            segment: round(sum(values) / len(values), 4) for segment, values in segments.items()
        }
        critical_pass = all(result.passed for result in results if result.critical)
        segment_pass = all(rate >= release_pass_rate for rate in segment_rates.values())
        return ReleaseReport(
            results=results,
            passed=critical_pass and segment_pass and pass_rate >= release_pass_rate,
            pass_rate=round(pass_rate, 4),
            segment_pass_rates=segment_rates,
        )
