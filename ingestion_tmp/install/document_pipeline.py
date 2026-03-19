from install.bundle_builder import build_bundle
from install.document_engine import generate_document
from install.latex_renderer import to_latex


def run(doc_type, topic, output_format, target):
    topic = (topic or "untitled").strip()
    md = generate_document(doc_type, topic)

    files = {
        f"payload/repo_root/docs/{topic}/paper.md": md
    }

    if output_format in ("md+tex", "full_bundle"):
        files[f"payload/repo_root/docs/{topic}/paper.tex"] = to_latex(md, topic)

    if output_format == "full_bundle":
        files[f"payload/repo_root/docs/{topic}/metadata.json"] = "{}"

    return build_bundle(topic, files, target)
