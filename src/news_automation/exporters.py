import csv
import json
from pathlib import Path

from .models import Article


FIELDS = ["title", "link", "description", "source", "published", "category", "summary"]


def export_json(articles: list[Article], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps([article.to_dict() for article in articles], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def export_csv(articles: list[Article], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for article in articles:
            writer.writerow(article.to_dict())
