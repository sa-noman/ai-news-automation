from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET
import html
import re

from .models import Article


TAG_RE = re.compile(r"<[^>]+>")


def _clean(value: str | None) -> str:
    if not value:
        return ""
    value = html.unescape(value)
    value = TAG_RE.sub(" ", value)
    return " ".join(value.split())


def _read_feed(location: str, timeout: float = 10.0) -> bytes:
    parsed = urlparse(location)
    if parsed.scheme in {"http", "https"}:
        request = Request(location, headers={"User-Agent": "ai-news-automation/1.0"})
        with urlopen(request, timeout=timeout) as response:
            return response.read()
    return Path(location).read_bytes()


def parse_feed(location: str, timeout: float = 10.0) -> list[Article]:
    """Parse a local or remote RSS/Atom feed into Article objects."""
    data = _read_feed(location, timeout=timeout)
    root = ET.fromstring(data)

    channel = root.find("channel")
    if channel is not None:
        source = _clean(channel.findtext("title"))
        articles = []
        for item in channel.findall("item"):
            articles.append(
                Article(
                    title=_clean(item.findtext("title")),
                    link=_clean(item.findtext("link")),
                    description=_clean(item.findtext("description")),
                    source=source,
                    published=_clean(item.findtext("pubDate")),
                )
            )
        return articles

    # Basic Atom support.
    ns = {"a": "http://www.w3.org/2005/Atom"}
    source = _clean(root.findtext("a:title", default="", namespaces=ns))
    articles = []
    for entry in root.findall("a:entry", ns):
        link_node = entry.find("a:link", ns)
        link = link_node.get("href", "") if link_node is not None else ""
        description = (
            entry.findtext("a:summary", default="", namespaces=ns)
            or entry.findtext("a:content", default="", namespaces=ns)
        )
        articles.append(
            Article(
                title=_clean(entry.findtext("a:title", default="", namespaces=ns)),
                link=_clean(link),
                description=_clean(description),
                source=source,
                published=_clean(entry.findtext("a:updated", default="", namespaces=ns)),
            )
        )
    return articles
