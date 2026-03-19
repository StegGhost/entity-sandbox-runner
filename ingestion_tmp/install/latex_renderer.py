def to_latex(md_text, title):
    safe_body = md_text.replace("\\", "\\\\")
    return f"""
\\documentclass[11pt]{{article}}
\\usepackage{{amsmath}}
\\usepackage[margin=1in]{{geometry}}
\\title{{{title}}}
\\author{{Rigel Randolph}}
\\date{{}}
\\begin{{document}}
\\maketitle

\\begin{{verbatim}}
{safe_body}
\\end{{verbatim}}

\\end{{document}}
"""
