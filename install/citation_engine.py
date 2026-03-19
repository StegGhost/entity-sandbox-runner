def inject_citations(doc_text, citations=None):
    citations = citations or []
    if not citations:
        return doc_text

    block = "\n\n## References\n" + "\n".join(f"- {c}" for c in citations)
    return doc_text + block
