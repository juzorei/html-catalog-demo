# HTML catalog parser demo

Extract product names and URLs from a saved HTML page. This offline example
uses synthetic markup; it does not scrape a protected website or bypass access
controls. It is a demo, not a client project.

```powershell
py -3 -X utf8 -m pip install -e '.[dev]'
py -3 -X utf8 -m pytest -q
py -3 -X utf8 parser.py example.html --base-url https://example.com/shop
```

The page contract is explicit: product links have class `product`. The parser
decodes entities, collects nested label text, resolves relative URLs and removes
duplicate URLs. Cross-origin and non-HTTP links are discarded. Script and style
contents do not contribute to product names.

This handles provided HTML, not JavaScript rendering, pagination or a changing
website schema. Adapt the page contract and fixtures for each permitted source.
