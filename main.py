import requests
from lxml import html
from xml.sax import saxutils
from urllib.parse import urlparse
from conference_scraper.scraper import ConferenceScraper

xscraper = ConferenceScraper('eng')

sessions = xscraper.get_sessions()
for url, name in sessions:
    print(f"[{name}]({url})")

for i in range(4):
    sess_url = f"{sessions[i][0]}"
    print('=' * 50)
    print('=' * 50)
    talks = xscraper.get_talks_for_session(sess_url)
    print(f"Found {len(talks)} talks for {sess_url}")
    for talk in talks:
        print('=' * 50)
        print(talk['title'])
        print(talk['speaker'])
        print(talk['url'])
        print(talk['img_src'])

    print('=' * 50)
    print('=' * 50)


