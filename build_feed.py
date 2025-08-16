import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import os

URL = "https://www.20minutos.es/autor/li-borja-teran/"

def main():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    fg = FeedGenerator()
    fg.id(URL)
    fg.title("Borja Terán en 20 Minutos")
    fg.link(href=URL, rel="alternate")
    fg.language("es")

    for article in soup.select("article a"):
        title = article.get_text(strip=True)
        link = article.get("href")
        if link and title:
            fe = fg.add_entry()
            fe.title(title)
            fe.link(href=link)

    os.makedirs("docs", exist_ok=True)
    fg.rss_file("docs/feed.xml")

if __name__ == "__main__":
    main()
