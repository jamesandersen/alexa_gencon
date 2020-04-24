import requests
from lxml import html
from urllib.parse import urlparse

GENERAL_CONF_ROOT_URL_TEMPLATE = "https://www.churchofjesuschrist.org/general-conference/conferences/?lang={}"

class HTTPException(Exception):
    pass

class GeneralConferenceClient:

    def __init__(self, lang):
        self.root_url = GENERAL_CONF_ROOT_URL_TEMPLATE.format(lang)
        parsed_url = urlparse(self.root_url)
        self.root_prefix = f"{parsed_url.scheme}://{parsed_url.hostname}"

    def get_sessions(self):
        response = requests.get(self.root_url)
        
        if response.status_code == 200:
            dom = html.fromstring(response.text)
            conf_links = dom.xpath('//a[@class="year-line__link"]')
            return [((f"{self.root_prefix}{link.xpath('./@href')[0]}", link.text.strip())) for link in conf_links]

        raise HTTPException(f"{self.root_url} yielded a {response.status_code} status code")

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

    def get_talk_detail(self, talk_url):
        talk_response = requests.get(talk_url)
        dom = html.fromstring(talk_response.content)
        mp3_link = dom.xpath('//a[starts-with(@class,"downloadLink-")]/@href')[0]
        video = dom.xpath('//video')[0]
        srcs = [{ 'type': 'mp3', 'src': mp3_link }]
        sources = video.xpath('//source')
        for source in sources:
            src = {}
            src['type'] = source.xpath('.//@type')[0]
            src['data-width'] = source.xpath('.//@data-width')[0]
            src['data-height'] = source.xpath('.//@data-height')[0]
            src['src'] = source.xpath('.//@src')[0] 
            srcs.append(src)
        return srcs



