# GitHub Trending Scraper

A Python script to fetch and display GitHub Trending projects.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from github_trending import fetch_trending

# Get daily trending projects
projects = fetch_trending()

# Or use the class directly
from github_trending import GitHubTrendingScraper
scraper = GitHubTrendingScraper(language="python", since="daily")
projects = scraper.fetch()
```

## Run from CLI

```bash
python main.py
```

## Parameters

- `language`: Programming language filter (e.g., "python", "go", "rust")
- `since`: Time range - "daily", "weekly", or "monthly"

## Output

Each project displays:
- Rank
- Repository name
- Stars, forks, today's stars
- Description
- Primary language
- URL
