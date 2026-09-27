import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from .models import Article


DEFAULT_CATEGORIES = {
    "Artificial Intelligence": ["artificial intelligence", "machine learning", "llm", "ai agent", "generative ai"],
    "Technology": ["technology", "software", "cybersecurity", "cloud", "chip", "python", "open source"],
    "World": ["world", "international", "global", "diplomacy", "summit"],
    "Business": ["business", "market", "economy", "company", "investment"],
    "Science": ["science", "research", "space", "climate", "health"],
}

SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def normalize_url(url: str) -> str:
    if not url:
        return ""
    parts = urlsplit(url.strip())
    # Ignore fragments and common tracking parameters for duplicate checks.
    query_parts = []
    for piece in parts.query.split("&"):
        if not piece:
            continue
        key = piece.split("=", 1)[0].lower()
        if key.startswith("utm_") or key in {"fbclid", "gclid"}:
            continue
        query_parts.append(piece)
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), "&".join(query_parts), ""))


def normalize_title(title: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9\s]", " ", title.lower()).split())


def deduplicate(articles: list[Article]) -> list[Article]:
    seen: set[str] = set()
    unique: list[Article] = []
    for article in articles:
        url_key = normalize_url(article.link)
        title_key = normalize_title(article.title)
        key = url_key or title_key
        if not key:
            continue
        if key in seen:
            continue
        seen.add(key)
        unique.append(article)
    return unique


def load_config(path: str | None = None) -> dict:
    config = {
        "categories": DEFAULT_CATEGORIES,
        "summary_sentences": 2,
        "telegram_max_chars": 900,
    }
    if not path:
        return config
    user = json.loads(Path(path).read_text(encoding="utf-8"))
    config.update(user)
    return config


def categorize(article: Article, categories: dict[str, list[str]]) -> str:
    haystack = f"{article.title} {article.description}".lower()
    best_category = "Other"
    best_score = 0
    for category, keywords in categories.items():
        score = sum(1 for keyword in keywords if keyword.lower() in haystack)
        if score > best_score:
            best_category = category
            best_score = score
    return best_category


def summarize_text(text: str, max_sentences: int = 2) -> str:
    clean = " ".join(text.split())
    if not clean:
        return ""
    sentences = [s.strip() for s in SENTENCE_RE.split(clean) if s.strip()]
    if not sentences:
        return clean
    return " ".join(sentences[:max_sentences])


def process_articles(articles: list[Article], config: dict) -> list[Article]:
    output = []
    for article in deduplicate(articles):
        article.category = categorize(article, config["categories"])
        base_text = article.description or article.title
        article.summary = summarize_text(base_text, int(config.get("summary_sentences", 2)))
        output.append(article)
    return output
