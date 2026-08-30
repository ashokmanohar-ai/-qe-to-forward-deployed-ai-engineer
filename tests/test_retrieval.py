from qe_fde.ai_service.retrieval import Document, InMemoryVectorStore, RAGAssistant


def _document(document_id: str, tenant: str, text: str) -> Document:
    return Document(
        document_id=document_id,
        tenant_id=tenant,
        source=f"{tenant}-manual",
        version="1",
        text=text,
    )


def test_search_is_always_tenant_scoped() -> None:
    store = InMemoryVectorStore()
    store.upsert(_document("a", "tenant-a", "Reset the device with the blue button."))
    store.upsert(_document("b", "tenant-b", "Reset the device with the secret red switch."))

    hits = store.search("How do I reset the device?", tenant_id="tenant-a", top_k=5)

    assert hits
    assert {hit.document.tenant_id for hit in hits} == {"tenant-a"}
    assert "secret red switch" not in hits[0].document.text


def test_rag_answer_cites_authorized_source() -> None:
    store = InMemoryVectorStore()
    store.upsert(_document("a", "demo", "Password reset links expire after fifteen minutes."))
    assistant = RAGAssistant(store)

    answer = assistant.ask("When does the password reset link expire?", tenant_id="demo")

    assert not answer.abstained
    assert answer.citations[0].document_id == "a"
    assert "fifteen minutes" in answer.text


def test_rag_abstains_without_authorized_context() -> None:
    store = InMemoryVectorStore()
    store.upsert(_document("a", "other", "Internal information."))
    answer = RAGAssistant(store).ask("What is the policy?", tenant_id="demo")
    assert answer.abstained
    assert answer.citations == ()
