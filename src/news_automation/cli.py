import argparse
from pathlib import Path

from .exporters import export_csv, export_json
from .formatter import build_digest
from .pipeline import load_config, process_articles
from .rss import parse_feed


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect, deduplicate, categorize, summarize, and export RSS news.")
    parser.add_argument("--feed", action="append", required=True, help="RSS/Atom URL or local XML file. Repeat for multiple feeds.")
    parser.add_argument("--config", help="Optional JSON config file.")
    parser.add_argument("--output", default="output", help="Output directory.")
    args = parser.parse_args()

    config = load_config(args.config)
    collected = []
    for feed in args.feed:
        collected.extend(parse_feed(feed))

    articles = process_articles(collected, config)
    output_dir = Path(args.output)
    export_json(articles, output_dir / "news.json")
    export_csv(articles, output_dir / "news.csv")
    (output_dir / "telegram_digest.txt").write_text(
        build_digest(articles, max_chars=int(config.get("telegram_max_chars", 900))),
        encoding="utf-8",
    )

    print(f"Collected: {len(collected)}")
    print(f"After deduplication: {len(articles)}")
    print(f"Output: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
