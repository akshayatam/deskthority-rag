import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify as md

BASE_URL = "https://deskthority.net"
CATEGORY_URL = f"{BASE_URL}/wiki/Category:Alps_SKCL/SKCM_series"
OUTPUT_DIR = Path("data/raw/deskthority")

USER_AGENT = "DeskthorityRAG/0.1 (research; contact: your-email@example.com)"

client = httpx.Client(
    headers={"User-Agent": USER_AGENT},
    follow_redirects=True,
    timeout=30,
)

robots = RobotFileParser()
robots.set_url(f"{BASE_URL}/robots.txt")
robots.read()


def fetch(url: str) -> BeautifulSoup:
    if not robots.can_fetch(USER_AGENT, url):
        raise PermissionError(f"Robots policy disallows: {url}")

    response = client.get(url)
    response.raise_for_status()

    time.sleep(2)  # Polite request spacing
    return BeautifulSoup(response.text, "html.parser")


def get_category_articles() -> list[tuple[str, str]]:
    soup = fetch(CATEGORY_URL)
    container = soup.select_one(".mw-category")

    if container is None:
        raise ValueError("Category article list not found")

    articles = []

    for anchor in container.select("a[href]"):
        title = anchor.get_text(" ", strip=True)
        url = urljoin(BASE_URL, anchor["href"])
        articles.append((title, url))

    return articles


def clean_article(soup: BeautifulSoup) -> str:
    content = soup.select_one(".mw-parser-output")

    if content is None:
        raise ValueError("Article content not found")

    # Remove non-article UI, but retain
    # specifications, tables, and references.
    for selector in [
        ".toc",
        ".mw-editsection",
        ".navbox",
        "script",
        "style",
    ]:
        for element in content.select(selector):
            element.decompose()

    # Convert relative links into absolute URLs.
    for element in content.select("[href], [src]"):
        for attribute in ("href", "src"):
            if element.has_attr(attribute):
                element[attribute] = urljoin(BASE_URL, element[attribute])

    markdown = md(
        str(content),
        heading_style="ATX",
        bullets="-",
    )

    # Reduce excessive blank lines.
    return re.sub(r"\n{3,}", "\n\n", markdown).strip()


def save_article(title: str, url: str) -> None:
    soup = fetch(url)
    content = clean_article(soup)

    slug = unquote(urlparse(url).path.split("/")[-1])
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", slug).strip("-")
    filename = f"{slug.lower()}.md"

    metadata = (
        "---\n"
        f'title: "{title.replace(chr(34), chr(39))}"\n'
        'source: "Deskthority Wiki"\n'
        f'url: "{url}"\n'
        'category: "Alps SKCL/SKCM series"\n'
        f'scraped_at: "{datetime.now(timezone.utc).isoformat()}"\n'
        "---\n\n"
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    path = OUTPUT_DIR / filename
    path.write_text(
        metadata + f"# {title}\n\n" + content + "\n",
        encoding="utf-8",
    )

    print(f"Saved: {path}")


def main() -> None:
    articles = get_category_articles()
    print(f"Found {len(articles)} articles")

    for title, url in articles:
        try:
            save_article(title, url)
        except (httpx.HTTPError, ValueError, PermissionError) as exc:
            print(f"Failed: {title} -> {exc}")


if __name__ == "__main__":
    try:
        main()
    finally:
        client.close()
