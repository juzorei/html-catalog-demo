import sqlite3
import pytest
from parser import parse_catalog

def test_html_parser_handles_entities_nested_text_and_relative_urls():
    html = '<a class="product" href="/p/1"><span>Tea &amp; Coffee</span></a><a class="product" href="/p/1">Duplicate</a><a href="/other">Ignore</a>'
    assert parse_catalog(html, "https://example.com/shop") == [{"name":"Tea & Coffee", "url":"https://example.com/p/1"}]

def test_html_parser_discards_cross_origin_and_script_links():
    html = '<a class="product" href="javascript:alert(1)">Bad</a><a class="product" href="https://evil.example/p">Other</a>'
    assert parse_catalog(html, "https://example.com") == []
