from collections import defaultdict

from .models import Article


def format_telegram_post(article: Article, max_chars: int = 900) -> str:
    parts = [
        f"📌 {article.category}",
        "",
        article.title.strip(),
    ]
    if article.summary:
        parts.extend(["", article.summary.strip()])
    if article.source:
        parts.extend(["", f"Source: {article.source}"])
    if article.link:
        parts.append(article.link)

    text = "\n".join(parts).strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "…"


def build_digest(articles: list[Article], max_chars: int = 900) -> str:
    grouped: dict[str, list[Article]] = defaultdict(list)
    for article in articles:
        grouped[article.category].append(article)

    blocks = []
    for category in sorted(grouped):
        blocks.append(f"## {category}")
        for article in grouped[category]:
            blocks.append(format_telegram_post(article, max_chars=max_chars))
    return "\n\n".join(blocks).strip() + ("\n" if blocks else "")
