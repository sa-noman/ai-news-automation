import csv
import json
import tempfile
import unittest
from pathlib import Path

from src.news_automation.exporters import export_csv, export_json
from src.news_automation.formatter import build_digest, format_telegram_post
from src.news_automation.models import Article
from src.news_automation.pipeline import (
    categorize,
    deduplicate,
    load_config,
    normalize_url,
    process_articles,
    summarize_text,
)
from src.news_automation.rss import parse_feed


ROOT = Path(__file__).resolve().parents[1]


class PipelineTests(unittest.TestCase):
    def test_parse_sample_feed(self):
        items = parse_feed(str(ROOT / "sample-data/feed.xml"))
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0].source, "Example Tech News")

    def test_normalize_url_removes_tracking(self):
        url = "https://Example.com/story/?utm_source=x&ref=home#section"
        self.assertEqual(normalize_url(url), "https://example.com/story?ref=home")

    def test_deduplicate(self):
        items = parse_feed(str(ROOT / "sample-data/feed.xml"))
        unique = deduplicate(items)
        self.assertEqual(len(unique), 2)

    def test_categorize(self):
        article = Article(title="New AI agent for workflow automation", link="https://example.com/a")
        category = categorize(article, load_config()["categories"])
        self.assertEqual(category, "Artificial Intelligence")

    def test_summary(self):
        text = "First sentence. Second sentence. Third sentence."
        self.assertEqual(summarize_text(text, 2), "First sentence. Second sentence.")

    def test_process_articles(self):
        items = parse_feed(str(ROOT / "sample-data/feed.xml"))
        processed = process_articles(items, load_config())
        self.assertEqual(len(processed), 2)
        self.assertTrue(all(item.summary for item in processed))

    def test_telegram_formatter(self):
        article = Article(
            title="Example story",
            link="https://example.com/story",
            source="Example",
            category="Technology",
            summary="Short summary.",
        )
        output = format_telegram_post(article)
        self.assertIn("📌 Technology", output)
        self.assertIn("Source: Example", output)

    def test_exports(self):
        article = Article(title="Story", link="https://example.com", category="World", summary="Summary")
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            export_json([article], base / "news.json")
            export_csv([article], base / "news.csv")
            data = json.loads((base / "news.json").read_text(encoding="utf-8"))
            self.assertEqual(data[0]["title"], "Story")
            with (base / "news.csv").open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["category"], "World")

    def test_digest(self):
        articles = [
            Article(title="A", link="https://a.example", category="Technology"),
            Article(title="B", link="https://b.example", category="World"),
        ]
        digest = build_digest(articles)
        self.assertIn("## Technology", digest)
        self.assertIn("## World", digest)


if __name__ == "__main__":
    unittest.main()
