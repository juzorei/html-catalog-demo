"""Extract a catalog from provided HTML. No browser or external requests."""
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit


def parse_catalog(html: str, base_url: str) -> list[dict]:
    base = urlsplit(base_url)
    if base.scheme not in {"https", "http"} or not base.netloc:
        raise ValueError("HTTP(S) base URL required")

    class Parser(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.current = None
            self.parts = []
            self.results = []
            self.seen = set()
            self.ignored = 0

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag in {"script", "style"}:
                self.ignored += 1
            if tag == "a":
                self.current, self.parts = None, []
                if "product" in attrs.get("class", "").split() and attrs.get("href"):
                    url = urljoin(base_url, attrs["href"])
                    parsed = urlsplit(url)
                    if parsed.scheme == base.scheme and parsed.netloc == base.netloc:
                        self.current = url

        def handle_data(self, text):
            if self.current and not self.ignored:
                self.parts.append(text)

        def handle_endtag(self, tag):
            if tag in {"script", "style"}:
                self.ignored = max(0, self.ignored-1)
            if tag == "a" and self.current:
                name = " ".join("".join(self.parts).split())
                if name and self.current not in self.seen:
                    self.results.append({"name":name,"url":self.current})
                    self.seen.add(self.current)
                self.current = None

    parser = Parser()
    parser.feed(html)
    parser.close()
    return parser.results


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser()
    parser.add_argument("html", type=Path)
    parser.add_argument("--base-url", required=True)
    args = parser.parse_args()
    print(json.dumps(parse_catalog(args.html.read_text(encoding="utf-8"), args.base_url), indent=2))
