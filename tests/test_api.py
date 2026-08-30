from fastapi.testclient import TestClient

from qe_fde.ai_service.api import create_app
from qe_fde.ai_service.config import Settings

API_KEY = "test-key-at-least-sixteen"


def _client() -> TestClient:
    return TestClient(create_app(Settings(api_key=API_KEY, environment="test")))


def test_health_is_public_but_v1_requires_auth() -> None:
    client = _client()
    assert client.get("/health").status_code == 200
    assert client.get("/v1/status").status_code == 401


def test_ingest_ask_and_tenant_isolation() -> None:
    client = _client()
    headers = {"X-API-Key": API_KEY}
    for tenant, text in (
        ("alpha", "Password reset links expire after fifteen minutes."),
        ("beta", "Beta uses a private recovery phrase."),
    ):
        response = client.post(
            "/v1/documents",
            headers=headers,
            json={
                "document_id": f"{tenant}-doc",
                "tenant_id": tenant,
                "source": f"{tenant}-manual",
                "version": "1",
                "text": text,
            },
        )
        assert response.status_code == 201

    answer = client.post(
        "/v1/ask",
        headers=headers,
        json={"tenant_id": "alpha", "question": "When does a reset link expire?"},
    )
    assert answer.status_code == 200
    payload = answer.json()
    assert "fifteen minutes" in payload["text"]
    assert "private recovery phrase" not in payload["text"]
    assert answer.headers["X-Correlation-ID"]


def test_agent_requires_confirmation_and_replays_side_effect() -> None:
    client = _client()
    headers = {"X-API-Key": API_KEY}
    body = {
        "tenant_id": "demo",
        "user_id": "learner",
        "calls": [{"name": "create_case", "arguments": {"subject": "Delayed order"}}],
        "idempotency_key": "request-1234",
    }
    denied = client.post("/v1/agent/run", headers=headers, json=body)
    assert denied.status_code == 400

    body["approved_tools"] = ["create_case"]
    first = client.post("/v1/agent/run", headers=headers, json=body)
    replay = client.post("/v1/agent/run", headers=headers, json=body)
    assert first.status_code == 200
    assert replay.json()["results"][0]["output"]["replayed"] is True


def test_evaluation_and_metrics_endpoints() -> None:
    client = _client()
    headers = {"X-API-Key": API_KEY}
    client.post(
        "/v1/documents",
        headers=headers,
        json={
            "document_id": "doc-1",
            "tenant_id": "demo",
            "source": "manual",
            "version": "1",
            "text": "Password reset links expire after fifteen minutes.",
        },
    )
    response = client.post(
        "/v1/evaluations/run",
        headers=headers,
        json={
            "cases": [
                {
                    "case_id": "case-1",
                    "tenant_id": "demo",
                    "question": "When does a password reset link expire?",
                    "expected_terms": ["fifteen minutes"],
                    "critical": True,
                }
            ]
        },
    )
    assert response.status_code == 200
    assert response.json()["passed"] is True
    metrics = client.get("/metrics", headers=headers)
    assert metrics.status_code == 200
    assert "fde_evaluation_runs_total" in metrics.text
