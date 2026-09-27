# AI News Automation

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Automation](https://img.shields.io/badge/Automation-News%20Pipeline-FF8A00)
![AI](https://img.shields.io/badge/AI-Summarization-6C63FF)

A practical Python project that collects RSS news, normalizes articles, removes duplicates, categorizes stories, creates concise summaries, and produces Telegram-ready output plus JSON/CSV exports.

## What It Does

```text
RSS / sample feeds
      ↓
Collect & normalize
      ↓
Deduplicate
      ↓
Categorize
      ↓
Summarize
      ↓
Format for Telegram
      ↓
Export JSON / CSV
```

The project works fully offline with sample data and a deterministic extractive summarizer. An optional OpenAI-compatible summarization path can be added later without changing the pipeline design.

## Features

- RSS/Atom-style feed collection
- URL/title normalization
- duplicate detection
- keyword-based news categorization
- concise extractive summaries
- Telegram-ready post formatting
- daily digest generation
- JSON and CSV export
- configuration through JSON
- CLI workflow
- automated unit tests
- GitHub Actions CI

## Repository Structure

```text
ai-news-automation/
├── src/news_automation/
│   ├── __init__.py
│   ├── models.py
│   ├── rss.py
│   ├── pipeline.py
│   ├── formatter.py
│   ├── exporters.py
│   └── cli.py
├── sample-data/
│   └── feed.xml
├── tests/
│   └── test_pipeline.py
├── config.example.json
├── .github/workflows/tests.yml
├── .gitignore
└── README.md
```

## Quick Start

Clone the repository and run the sample feed:

```bash
git clone https://github.com/sa-noman/ai-news-automation.git
cd ai-news-automation
python -m src.news_automation.cli --feed sample-data/feed.xml --output output
```

Generated files:

```text
output/
├── news.json
├── news.csv
└── telegram_digest.txt
```

## Example Output

```text
📌 Technology

Open-source AI tooling gains new automation features.

A new release adds workflow automation and local processing improvements.

Source: Example Tech
```

## Configuration

Copy the example configuration if you want to customize categories:

```bash
cp config.example.json config.json
```

The CLI accepts a local XML file or an HTTP/HTTPS RSS URL.

## Tests

Run:

```bash
python -m unittest discover -s tests -v
```

## Responsible Use

This project automates collection and formatting. It does not guarantee that a claim is accurate. Important stories should be checked against the original source and, where appropriate, corroborated with additional reliable sources before publication.

## Future Improvements

- optional LLM provider integration
- multilingual summaries
- semantic duplicate detection
- scheduled Telegram delivery
- source reliability metadata
- richer topic models
- web dashboard
