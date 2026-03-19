from install.document_engine import generate_document
from install.latex_renderer import to_latex
from install.bundle_builder import build_bundle


def run(doc_type, topic, output_format, target):
    md = generate_document(doc_type, topic)

    files = {
        f"payload/repo_root/docs/{topic}/paper.md": md
    }

    if "tex" in output_format:
        tex = to_latex(md, topic)
        files[f"payload/repo_root/docs/{topic}/paper.tex"] = tex

    if output_format == "full_bundle":
        files[f"payload/repo_root/docs/{topic}/metadata.json"] = "{}"

    return build_bundle(topic, files, target)
