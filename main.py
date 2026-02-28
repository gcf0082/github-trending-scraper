#!/usr/bin/env python3
from scraper import fetch_trending


def main():
    print("=" * 60)
    print("GitHub Trending Daily Top Projects")
    print("=" * 60)
    print()

    projects = fetch_trending()

    for p in projects:
        print(f"{p.rank:2}. {p.name}")
        print(f"    ⭐ {p.stars:>6,} | 🍴 {p.forks:>5,} | 📈 +{p.today_stars:>4} today")
        if p.description:
            desc = p.description[:70] + "..." if len(p.description) > 70 else p.description
            print(f"    {desc}")
        if p.language:
            print(f"    🏷️  {p.language}")
        print(f"    🔗 {p.url}")
        print()


if __name__ == "__main__":
    main()
