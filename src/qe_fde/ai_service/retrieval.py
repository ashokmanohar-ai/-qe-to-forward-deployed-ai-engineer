"""Deterministic, dependency-free retrieval used for local learning.

This implementation is deliberately small. It makes retrieval, tenant filters,
citations, and evaluation inspectable before learners replace it with a managed
embedding and vector database stack.
"""

from __future__ import annotations

import hashlib
import math
import re
import threading
from dataclasses import dataclass, field

_TOKEN = re.compile(r"[a-z0-9]+")


class RetrievalError(ValueError):
    """A retrieval request or document violates the service contract."""


def _tokens(text: str) -> list[str]:
    return _TOKEN.findall(text.casefold())


class HashEmbedding:
    """Feature-hashing bag-of-words embedding for a zero-cost local demo."""

    def __init__(self, dimensions: int = 128) -> None:
        if dimensions < 16:
            raise ValueError("dimensions must be at least 16")
        self.dimensions = dimensions

    def embed(self, text: str) -> tuple[float, ...]:
        vector = [0.0] * self.dimensions
        for token in _tokens(text):
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign
        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return tuple(vector)
        return tuple(value / norm for value in vector)


def cosine(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    if len(left) != len(right):
        raise ValueError("vectors must have the same dimensions")
    return sum(a * b for a, b in zip(left, right, strict=True))


@dataclass(frozen=True)
class Document:
    document_id: str
    tenant_id: str
    source: str
    version: str
    text: str
    metadata: dict[str, str] = field(default_factory=dict)

    def validate(self) -> None:
        for field_name, value in (
            ("document_id", self.document_id),
            ("tenant_id", self.tenant_id),
            ("source", self.source),
            ("version", self.version),
            ("text", self.text),
        ):
            if not value.strip():
                raise RetrievalError(f"{field_name} must not be empty")
        if len(self.text) > 100_000:
            raise RetrievalError("document text exceeds the local demo limit")


@dataclass(frozen=True)
class SearchHit:
    document: Document
    score: float


@dataclass(frozen=True)
class Citation:
    document_id: str
    source: str
    version: str
    score: float


@dataclass(frozen=True)
class Answer:
    text: str
    citations: tuple[Citation, ...]
    abstained: bool
    reason: str | None = None


class InMemoryVectorStore:
    """Thread-safe store that always scopes search to a tenant."""

    def __init__(
        self, *, max_documents: int = 1000, embedding: HashEmbedding | None = None
    ) -> None:
        if max_documents < 1:
            raise ValueError("max_documents must be positive")
        self.max_documents = max_documents
        self.embedding = embedding or HashEmbedding()
        self._documents: dict[tuple[str, str], tuple[Document, tuple[float, ...]]] = {}
        self._lock = threading.RLock()

    def upsert(self, document: Document) -> None:
        document.validate()
        key = (document.tenant_id, document.document_id)
        vector = self.embedding.embed(document.text)
        with self._lock:
            if key not in self._documents and len(self._documents) >= self.max_documents:
                raise RetrievalError("document capacity reached")
            self._documents[key] = (document, vector)

    def count(self, tenant_id: str | None = None) -> int:
        with self._lock:
            if tenant_id is None:
                return len(self._documents)
            return sum(key[0] == tenant_id for key in self._documents)

    def search(self, question: str, *, tenant_id: str, top_k: int = 3) -> tuple[SearchHit, ...]:
        if not question.strip():
            raise RetrievalError("question must not be empty")
        if not tenant_id.strip():
            raise RetrievalError("tenant_id must not be empty")
        if not 1 <= top_k <= 20:
            raise RetrievalError("top_k must be between 1 and 20")
        query = self.embedding.embed(question)
        with self._lock:
            candidates = [
                SearchHit(document=document, score=cosine(query, vector))
                for (stored_tenant, _), (document, vector) in self._documents.items()
                if stored_tenant == tenant_id
            ]
        candidates.sort(key=lambda hit: (-hit.score, hit.document.document_id))
        return tuple(candidates[:top_k])


class RAGAssistant:
    """Retrieval plus deterministic grounded synthesis and abstention."""

    def __init__(self, store: InMemoryVectorStore, *, minimum_score: float = 0.05) -> None:
        self.store = store
        self.minimum_score = minimum_score

    def ask(self, question: str, *, tenant_id: str, top_k: int = 3) -> Answer:
        hits = self.store.search(question, tenant_id=tenant_id, top_k=top_k)
        relevant = tuple(hit for hit in hits if hit.score >= self.minimum_score)
        if not relevant:
            return Answer(
                text="I do not have enough authorized evidence to answer that question.",
                citations=(),
                abstained=True,
                reason="no_relevant_authorized_context",
            )
        excerpts: list[str] = []
        citations: list[Citation] = []
        for hit in relevant:
            compact = " ".join(hit.document.text.split())
            excerpts.append(f"[{hit.document.source} v{hit.document.version}] {compact[:280]}")
            citations.append(
                Citation(
                    document_id=hit.document.document_id,
                    source=hit.document.source,
                    version=hit.document.version,
                    score=round(hit.score, 4),
                )
            )
        return Answer(
            text="Based on the authorized sources: " + " ".join(excerpts),
            citations=tuple(citations),
            abstained=False,
        )
