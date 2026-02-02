import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import hashlib

URL = "https://scrap.tf/raffles"
OUT = "rss.xml"

r = requests.get(URL, timeout=30)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

fg = FeedGenerator()
fg.title("scrap.tf raffles")
fg.link(href=URL)
fg.description("New raffles on scrap.tf")

seen = set()

for a in soup.select("a[href^='/raffles/']"):
    title = a.text.strip()
    if not title:
        continue

    link = "https://scrap.tf" + a["href"]
    if link in seen:
        continue
    seen.add(link)

    fe = fg.add_entry()
    fe.id(hashlib.md5(link.encode()).hexdigest())
    fe.title(title)
    fe.link(href=link)

fg.rss_file(OUT)
