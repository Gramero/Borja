import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone
from email.utils import format_datetime
from xml.sax.saxutils import escape
import os

AUTHOR_URL = "https://www.20minutos.es/autor/li-borja-teran/"
BASE = "https://www.20minutos.es"
OUT = "docs/feed.xml"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}

def main():
    try:
        r = requests.get(AUTHOR_URL, headers=HEADERS, timeout=30)
        r.raise_for_status()
    except Exception as e:
        os.makedirs("docs", exist_ok=True)
        with open(OUT, "w", encoding="utf-8") as f:
            f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>Borja Terán - 20minutos</title>
<link>{AUTHOR_URL}</link>
<description>Error al obtener la página: {escape(str(e))}</description>
</channel></rss>""")
        return

    soup = BeautifulSoup(r.text, "html.parser")

    # coger solo enlaces correctos en titulares
    items = []
    seen = set()
    for a in soup.select("h2.media-title a[href]"):
        href = a.get("href")
        if not href:
            continue
        if "/noticia/" not in href:   # filtramos ruido
            continue
        link = href if href.startswith("http") else urljoin(BASE, href)
        if link in seen:
            continue
        title = a.get_text(strip=True)
        if not title or len(title) < 6:
            continue
        seen.add(link)
        items.append((title, link))
        if len(items) == 5:           # solo los 5 últimos
            break

    # construir RSS
    now = format_datetime(datetime.now(timezone.utc))
    rss_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0"><channel>',
        f"<title>Borja Terán - 20minutos (no oficial)</title>",
        f"<link>{AUTHOR_URL}</link>",
        "<description>Últimos 5 artículos del autor</description>",
        f"<lastBuildDate>{now}</lastBuildDate>",
    ]
    for title, link in items:
        rss_parts.append(
            "<item>"
            f"<title>{escape(title)}</title>"
            f"<link>{escape(link)}</link>"
            f"<guid>{escape(link)}</guid>"
            "</item>"
        )
    rss_parts.append("</channel></rss>")

    os.makedirs("docs", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("".join(rss_parts))

if __name__ == "__main__":
    main()
