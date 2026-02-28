#!/usr/bin/env python3
import json
from datetime import datetime
from scraper import GitHubTrendingScraper


def save_to_json(all_projects, filename):
    data = {
        "timestamp": datetime.now().isoformat(),
        "count": len(all_projects),
        "projects": all_projects
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(all_projects)} unique projects to {filename}")


def main():
    categories = ["daily", "weekly", "monthly"]
    category_names = {"daily": "日榜", "weekly": "周榜", "monthly": "月榜"}

    all_projects = []
    seen = set()

    for since in categories:
        print(f"Fetching {category_names[since]}...")
        scraper = GitHubTrendingScraper(since=since)
        projects = scraper.fetch_with_details()
        
        for p in projects:
            if p.name not in seen:
                seen.add(p.name)
                all_projects.append({
                    "name": p.name,
                    "description": p.description,
                    "language": p.language,
                    "stars": p.stars,
                    "forks": p.forks,
                    "today_stars": p.today_stars,
                    "url": p.url,
                    "created_at": p.created_at,
                    "updated_at": p.updated_at
                })

    save_to_json(all_projects, "github_trending.json")


if __name__ == "__main__":
    main()
