import shutil
import subprocess


def render_pdf_from_markdown(markdown_path, output_pdf_path):
    pandoc = shutil.which("pandoc")
    if not pandoc:
        return {
            "ok": False,
            "reason": "pandoc_not_found",
            "markdown_path": markdown_path,
            "output_pdf_path": output_pdf_path
        }

    cmd = [pandoc, markdown_path, "-o", output_pdf_path]
    completed = subprocess.run(cmd, capture_output=True, text=True)

    return {
        "ok": completed.returncode == 0,
        "reason": "success" if completed.returncode == 0 else "pandoc_failed",
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "markdown_path": markdown_path,
        "output_pdf_path": output_pdf_path
    }
