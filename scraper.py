import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TrendingProject:
    rank: int
    name: str
    description: str
    language: Optional[str]
    stars: int
    forks: int
    today_stars: int
    url: str


class GitHubTrendingScraper:
    BASE_URL = "https://github.com/trending"

    def __init__(self, language: str = "", since: str = "daily"):
        self.language = language
        self.since = since
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def get_url(self) -> str:
        url = self.BASE_URL
        if self.language:
            url += f"/{self.language}"
        return url

    def fetch(self) -> List[TrendingProject]:
        url = self.get_url()
        params = {"since": self.since} if self.since else None

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("article.Box-row")

        projects = []
        for rank, article in enumerate(articles, 1):
            project = self._parse_article(article, rank)
            if project:
                projects.append(project)

        return projects

    def _parse_article(self, article, rank: int) -> Optional[TrendingProject]:
        try:
            h2 = article.select_one("h2")
            if not h2:
                return None

            links = h2.select("a")
            if not links:
                return None

            repo_link = links[0]
            repo_path = repo_link.get("href", "").strip()
            name = repo_path.lstrip("/")
            url = f"https://github.com{repo_path}"

            description_elem = article.select_one("p")
            description = description_elem.get_text(strip=True) if description_elem else ""

            spans = article.select("span")
            language = None
            stars = 0
            forks = 0
            today_stars = 0

            text_content = article.get_text()

            import re
            lang_match = re.search(r'([A-Za-z+#]+)\s+[\d,]+', text_content)
            if lang_match:
                potential_lang = lang_match.group(1)
                if potential_lang.lower() not in ['star', 'fork', 'built', 'by']:
                    language = potential_lang

            for span in spans:
                span_text = span.get_text(strip=True)
                if "stars today" in span_text:
                    today_stars = self._parse_number(span_text.replace("stars today", "").strip())

            all_text = article.get_text()
            lines = [line.strip() for line in all_text.split('\n') if line.strip()]
            
            stars_val = None
            forks_val = None
            for i, line in enumerate(lines):
                if line.replace(",", "").isdigit():
                    if stars_val is None:
                        stars_val = int(line.replace(",", ""))
                    elif forks_val is None:
                        forks_val = int(line.replace(",", ""))
                        break

            if stars_val:
                stars = stars_val
            if forks_val:
                forks = forks_val

            return TrendingProject(
                rank=rank,
                name=name,
                description=description,
                language=language,
                stars=stars,
                forks=forks,
                today_stars=today_stars,
                url=url
            )
        except Exception as e:
            print(f"Error parsing article: {e}")
            return None

    def _parse_number(self, text: str) -> int:
        text = text.replace(",", "").strip()
        multipliers = {"k": 1000, "K": 1000, "m": 1000000, "M": 1000000}
        for suffix, multiplier in multipliers.items():
            if suffix in text:
                return int(float(text.replace(suffix, "")) * multiplier)
        try:
            return int(text)
        except ValueError:
            return 0


def fetch_trending(language: str = "", since: str = "daily") -> List[TrendingProject]:
    scraper = GitHubTrendingScraper(language=language, since=since)
    return scraper.fetch()


if __name__ == "__main__":
    projects = fetch_trending()
    for p in projects:
        print(f"{p.rank}. {p.name}")
        print(f"   ⭐ {p.stars} | 🍴 {p.forks} | 📈 +{p.today_stars} today")
        print(f"   {p.description[:80]}..." if len(p.description) > 80 else f"   {p.description}")
        print(f"   🔗 {p.url}")
        print()
