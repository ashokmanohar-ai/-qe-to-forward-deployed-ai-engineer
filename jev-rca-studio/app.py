import io
import json
import os
import zipfile
from collections import Counter

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

PRODUCT = "JEV RCA Studio"
VERSION = "1.0.0"
JEV_API_URL = os.getenv("JEV_API_URL", "https://api.typesafe.ai/v1/systemone")
JEV_MODEL = os.getenv("JEV_MODEL", "jev-latest")


def load_report(upload):
    raw = upload.read()
    name = (upload.filename or "").lower()
    docs = []

    if name.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            for member in archive.namelist():
                if member.lower().endswith(".json") and not member.endswith("/"):
                    try:
                        docs.append(
                            (
                                member,
                                json.loads(
                                    archive.read(member).decode(
                                        "utf-8", errors="replace"
                                    )
                                ),
                            )
                        )
                    except Exception:
                        pass
        if not docs:
            raise ValueError("ZIP does not contain a readable JSON report.")
        return docs

    try:
        return [
            (
                upload.filename or "report.json",
                json.loads(raw.decode("utf-8", errors="replace")),
            )
        ]
    except Exception as exc:
        raise ValueError(
            "Upload a valid Playwright JSON report or ZIP containing JSON reports."
        ) from exc


def collect_failures(obj, path="root", out=None):
    out = out if out is not None else []

    if isinstance(obj, dict):
        title = obj.get("title") or obj.get("name") or obj.get("testId") or path
        status = str(
            obj.get("status")
            or obj.get("outcome")
            or obj.get("expectedStatus")
            or ""
        ).lower()
        error = obj.get("error") or obj.get("errors")

        if status in {"failed", "timedout", "timed_out", "unexpected"} or error:
            message = ""
            if isinstance(error, dict):
                message = str(error.get("message") or error.get("stack") or error)
            elif isinstance(error, list):
                message = " | ".join(
                    str(item.get("message") if isinstance(item, dict) else item)
                    for item in error[:3]
                )
            elif error:
                message = str(error)

            out.append(
                {
                    "title": str(title),
                    "status": status or "failed",
                    "error": message[:1800],
                    "path": path,
                }
            )

        for key, value in obj.items():
            if key not in {"error", "errors"}:
                collect_failures(value, f"{path}.{key}", out)

    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            collect_failures(value, f"{path}[{index}]", out)

    return out


def heuristic_category(text):
    value = text.lower()

    if any(
        token in value
        for token in [
            "timeout",
            "timed out",
            "net::",
            "econn",
            "dns",
            "503",
            "502",
            "service unavailable",
        ]
    ):
        return "Environment issue"

    if any(
        token in value
        for token in [
            "locator",
            "strict mode",
            "element",
            "click",
            "fill",
            "expect(",
            "selector",
            "detached",
        ]
    ):
        return "Automation issue"

    if any(
        token in value
        for token in [
            "fixture",
            "test data",
            "token expired",
            "401",
            "403",
            "seed",
            "record not found",
        ]
    ):
        return "Test-data problem"

    if any(token in value for token in ["retry", "flaky", "intermittent"]):
        return "Flaky test"

    return "Likely product defect"


def summarize(docs):
    failures = []

    for source_name, document in docs:
        for failure in collect_failures(document):
            failure["source"] = source_name
            failures.append(failure)

    unique = []
    seen = set()

    for failure in failures:
        signature = (failure["title"], failure["error"][:200])
        if signature not in seen:
            seen.add(signature)
            unique.append(failure)

    failures = unique[:40]
    counts = Counter(
        heuristic_category(f'{failure["title"]} {failure["error"]}')
        for failure in failures
    )

    return {
        "files_parsed": len(docs),
        "failure_count": len(failures),
        "category_counts": dict(counts),
        "failures": failures[:12],
    }


def call_jev(api_key, report_summary):
    payload = {
        "model": JEV_MODEL,
        "state": {
            "task": "Playwright test failure root cause analysis",
            "product": PRODUCT,
            "report_summary": report_summary,
            "instructions": (
                "Classify failures into likely product defect, automation issue, "
                "environment issue, flaky test, or test-data problem. "
                "Return concise RCA and recommended next actions."
            ),
        },
        "questions": [
            {
                "id": "category",
                "type": "choice",
                "question": "What is the most likely dominant root-cause category?",
                "choices": [
                    "Likely product defect",
                    "Automation issue",
                    "Environment issue",
                    "Flaky test",
                    "Test-data problem",
                ],
            },
            {
                "id": "confidence",
                "type": "score",
                "question": "How confident are you in the RCA from 0 to 100?",
                "min": 0,
                "max": 100,
            },
            {
                "id": "evidence_sufficient",
                "type": "noul",
                "question": (
                    "Is the supplied evidence sufficient for a useful root-cause "
                    "assessment?"
                ),
            },
        ],
    }

    response = requests.post(
        JEV_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=45,
    )

    try:
        data = response.json()
    except Exception:
        data = {"raw_text": response.text[:4000]}

    return response.status_code, data


@app.get("/")
def index():
    return render_template("index.html", product=PRODUCT, version=VERSION)


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "product": PRODUCT,
            "version": VERSION,
            "jev_model": JEV_MODEL,
        }
    )


@app.post("/api/test-key")
def test_key():
    body = request.get_json(silent=True) or {}
    api_key = (
        body.get("api_key") or os.getenv("TYPESAFE_API_KEY") or ""
    ).strip()

    if not api_key:
        return (
            jsonify(
                {
                    "ok": False,
                    "message": "Enter a JEV / TypeSafe AI API key.",
                }
            ),
            400,
        )

    payload = {
        "model": JEV_MODEL,
        "state": {
            "task": "connection test",
            "input": "JEV RCA Studio connectivity check",
        },
        "questions": [
            {
                "id": "connected",
                "type": "noul",
                "question": "Is this a valid connection test request?",
            }
        ],
    }

    try:
        response = requests.post(
            JEV_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=25,
        )
        return jsonify(
            {
                "ok": response.ok,
                "status": response.status_code,
                "message": (
                    "Connection successful."
                    if response.ok
                    else f"JEV returned HTTP {response.status_code}"
                ),
            }
        )
    except Exception as exc:
        return jsonify({"ok": False, "message": str(exc)}), 502


@app.post("/api/analyze")
def analyze():
    api_key = (
        request.form.get("api_key") or os.getenv("TYPESAFE_API_KEY") or ""
    ).strip()
    upload = request.files.get("report")

    if not upload:
        return jsonify({"error": "Choose a Playwright JSON report or ZIP."}), 400

    try:
        docs = load_report(upload)
        report_summary = summarize(docs)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    heuristic_rca = [
        {
            "title": failure["title"],
            "source": failure["source"],
            "category": heuristic_category(
                f'{failure["title"]} {failure["error"]}'
            ),
            "evidence": failure["error"][:500],
        }
        for failure in report_summary["failures"]
    ]

    result = {
        "summary": report_summary,
        "heuristic_rca": heuristic_rca,
        "jev": None,
    }

    if api_key:
        try:
            status, data = call_jev(api_key, report_summary)
            result["jev"] = {"http_status": status, "response": data}
        except Exception as exc:
            result["jev"] = {"error": str(exc)}

    return jsonify(result)


@app.errorhandler(413)
def file_too_large(_):
    return (
        jsonify(
            {
                "error": (
                    "File too large. Uploads are limited to 10 MB."
                )
            }
        ),
        413,
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8080")),
        debug=False,
    )
