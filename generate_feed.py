import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

FEED_PATH = "docs/feed.xml"
SITE_URL = "https://borjateran.com/"  # URL del blog

def fetch_articles():
    resp = requests.get(SITE_URL, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Adaptado al HTML típico de WordPress
    posts = soup.select("article h2 a, article h3 a")[:5]

    articles = []
    for post in posts:
        title = post.get_text(strip=True)
        link = post.get("href")
        if not link.startswith("http"):
            link = SITE_URL.rstrip("/") + "/" + link.lstrip("/")
        articles.append({"title": title, "link": link})
    return articles

def generate_rss(articles):
    now = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
    rss_items = ""
    for art in articles:
        rss_items += f"""
        <item>
            <title>{art['title']}</title>
            <link>{art['link']}</link>
            <pubDate>{now}</pubDate>
        </item>"""

    rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
      <channel>
        <title>Borja Terán - Últimos artículos</title>
        <link>{SITE_URL}</link>
        <description>RSS feed generado automáticamente</description>
        <lastBuildDate>{now}</lastBuildDate>
        {rss_items}
      </channel>
    </rss>
    """
    return rss

def save_feed(rss):
    os.makedirs(os.path.dirname(FEED_PATH), exist_ok=True)
    with open(FEED_PATH, "w", encoding="utf-8") as f:
        f.write(rss)

if __name__ == "__main__":
    articles = fetch_articles()
    rss = generate_rss(articles)
    save_feed(rss)
    print(f"Feed actualizado con {len(articles)} artículos.")
