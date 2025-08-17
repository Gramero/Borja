import requests
from bs4 import BeautifulSoup
import datetime

URL = "https://www.20minutos.es/autor/li-borja-teran/"
FEED_PATH = "docs/feed.xml"

def fetch_articles():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    articles = []
    for item in soup.select("article")[:5]:  # solo 5 últimos
        title_tag = item.select_one("h2 a")
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)
        link = title_tag["href"]
        if not link.startswith("http"):
            link = "https://www.20minutos.es" + link
        articles.append((title, link))

    return articles

def generate_rss(articles):
    now = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
<title>Borja Terán - 20minutos (no oficial)</title>
<link>{URL}</link>
<description>Últimos artículos de Borja Terán</description>
<lastBuildDate>{now}</lastBuildDate>
"""

    for title, link in articles:
        rss += f"""
<item>
<title>{title}</title>
<link>{link}</link>
<guid>{link}</guid>
<pubDate>{now}</pubDate>
</item>
"""
    rss += "</channel></rss>"
    return rss

if __name__ == "__main__":
    articles = fetch_articles()
    rss_content = generate_rss(articles)
    with open(FEED_PATH, "w", encoding="utf-8") as f:
        f.write(rss_content)
    print("RSS actualizado correctamente")
