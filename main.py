import requests
from lxml import html
from xml.sax import saxutils
from urllib.parse import urlparse
from gencon.conference_client import GeneralConferenceClient

conf_client = GeneralConferenceClient('eng')

sessions = conf_client.get_sessions()
for url, name in sessions:
    print(f"[{name}]({url})")

for i in range(4):
    sess_url = f"{sessions[i][0]}"
    print('=' * 50)
    print('=' * 50)
    talks = conf_client.get_talks_for_session(sess_url)
    print(f"Found {len(talks)} talks for {sess_url}")
    for talk in talks:
        detail = conf_client.get_talk_detail(talk['url'])
        print('=' * 50)
        print(talk['title'])
        print(talk['speaker'])
        print(talk['url'])
        print(talk['img_src'])
        print('=== Media ===')
        for src in detail:
            print(f"{src['type']} = {src['src']}")

    print('=' * 50)
    print('=' * 50)


