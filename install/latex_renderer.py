def to_latex(md_text, title):
    return f"""
\\documentclass{{article}}
\\begin{{document}}

\\title{{{title}}}
\\author{{Rigel Randolph}}
\\maketitle

{md_text}

\\end{{document}}
"""
