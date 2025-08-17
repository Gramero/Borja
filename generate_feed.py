import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.20minutos.es/autor/li-borja-teran/"
OUTPUT_FILE = "docs/feed.xml"

def main():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    # Buscar artículos
    articles = soup.select("article a")
    seen = set()
    items = []
    for a in articles:
        link = a.get("href")
        title = a.get_text(strip=True)
        if link and title and link not in seen:
            seen.add(link)
            if not link.startswith("http"):
                link = "https://www.20minutos.es" + link
            items.append((title, link))
        if len(items) >= 5:
            break

    # Crear feed RSS
    rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
<title>Borja Terán - 20Minutos</title>
<link>{URL}</link>
<description>Últimos artículos de Borja Terán</description>
<lastBuildDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}</lastBuildDate>
"""
    for title, link in items:
        rss += f"""
<item>
<title>{title}</title>
<link>{link}</link>
<guid>{link}</guid>
</item>
"""
    rss += "</channel></rss>"

    # Guardar en docs/feed.xml
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(rss)

if __name__ == "__main__":
    main()
