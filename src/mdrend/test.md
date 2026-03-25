# MDRend - Python Markdown Renderer in the browser
This tool will be run as follows:
```bash
uv run mdrend <filename>
```
```python
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

```
