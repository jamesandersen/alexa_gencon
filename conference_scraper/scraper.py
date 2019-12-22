import requests
from lxml import html
from urllib.parse import urlparse

class ConferenceScraper:

    def __init__(self, lang):
        self.root_url = f"https://www.churchofjesuschrist.org/general-conference/conferences/?lang={lang}"
        parsed_url = urlparse(self.root_url)
        self.root_prefix = f"{parsed_url.scheme}://{parsed_url.hostname}"

    def get_sessions(self):
        response = requests.get(self.root_url)
        dom = html.fromstring(response.content)
        conf_links = dom.xpath('//a[@class="year-line__link"]')
        return [((f"{self.root_prefix}{link.xpath('./@href')[0]}", link.text.strip())) for link in conf_links]

    def get_talks_for_session(self, session_url):
        sess_response = requests.get(session_url)
        dom = html.fromstring(sess_response.content)
        talk_links = dom.xpath('//div[@class="lumen-tile lumen-tile--horizontal lumen-tile--list"]')
        talks = []
        for talk in talk_links:
            img_src = talk.xpath('.//picture/img[@class="lumen-image__image"]/@data-src')[0]
            speaker = talk.xpath('.//picture/img[@class="lumen-image__image"]/@alt')[0]
            title = talk.xpath('.//div[@class="lumen-tile__title"]/div/text()')[0]
            talk_rel_url = talk.xpath('.//a[@class="lumen-tile__link"]/@href')[0]
            talk_url = f"{self.root_prefix}{talk_rel_url}"
            talks.append({
                "title": title,
                "speaker": speaker,
                "url": talk_url,
                "img_src": img_src
            })
        return talks



