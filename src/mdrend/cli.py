import argparse
import sys
import subprocess
import tempfile
import os
import mistune
from jinja2 import Template
from pygments import highlight
from pathlib import Path
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter, html
from pygments.util import ClassNotFound
from importlib import resources

class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        if info:
            try:
                lexer = get_lexer_by_name(info, stripall=True)
            except ClassNotFound:
                lexer = guess_lexer(code)
        else:
            lexer = guess_lexer(code)
        
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("render", help="render markdown file via cli")
    parser.add_argument("--watch", help="continuously watch markdown file and edit realtime")
    args = parser.parse_args()
    
    md = mistune.create_markdown(renderer=HighlightRenderer())
    pygments_css = HtmlFormatter(style="github-dark").get_style_defs(".highlight")
    template = resources.files("mdrend").joinpath("templates/template.html").read_text()
    html_body = md(Path(args.render).read_text())
    output = Template(template).render(pygments_css=pygments_css, html_body=html_body) 
    if not args.watch:
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode='w') as write_file:
            write_file.write(output)
            tmp_path = write_file.name

        subprocess.run(["open", tmp_path])


if __name__ == "__main__":
    sys.exit(main())
