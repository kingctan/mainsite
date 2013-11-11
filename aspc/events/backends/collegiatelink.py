import requests
import xml.etree.ElementTree as ET
import logging
from datetime import datetime
from HTMLParser import HTMLParser
import re

logger = logging.getLogger(__name__)

class CollegiateLinkBackend(object):
    rss_url = 'https://claremont.collegiatelink.net/EventRss/EventsRss';

    def _get_rss(self):
        events_xml_tree = requests.get(self.rss_url).text
        return ET.fromstring(events_xml_tree)

    def get_events_data(self):
        normalized_events = []

        events_xml_root = self._get_rss()

        for item in events_xml_root.iter('item'):
            event = {
                'name': item.find('title').text,
                'url': item.find('link').text,
            }

            # CollegiateLink provides poorly-formed HTML in its RSS feed, so it is necessary to further parse it
            parser = CollegiateLinkHTMLParser()
            parser.feed(item.find('description').text)
            event['start'] = datetime.strptime(parser.parsed_data['start'], '%A, %B %d, %Y (%H:%M %p)')
            event['location'] = parser.parsed_data['location']
            event['description'] = parser.parsed_data['description']

            # The host is oddly wrapped inside of parentheses... need to extract it
            event['host'] = (re.search(r'\((.*?)\)', item.find('author').text)).group(1)

            normalized_events.append(event)

        return normalized_events


class CollegiateLinkHTMLParser(HTMLParser):
    parsed_data = {
        'start': '',
        'location': '',
        'description': ''
    }
    __current_state = None

    def handle_starttag(self, tag, attrs):
        if ('class', 'dtstart') in attrs:
            self.__current_state = 'start'
        elif ('class', 'location') in attrs:
            self.__current_state = 'location'
        elif ('class', 'description') in attrs:
            self.__current_state = 'description'
        else:
            if self.__current_state != 'description': # The description block has a lot of tags inside of it, so this captures nested information
                self.__current_state = ''

    def handle_endtag(self, tag):
        if self.__current_state != 'description': # The description block has a lot of tags inside of it, so this captures nested information
            self.__current_state = ''

    def handle_data(self, data):
        if self.__current_state == 'start':
            self.parsed_data['start'] = data
        elif self.__current_state == 'location':
            self.parsed_data['location'] = data
        elif self.__current_state == 'description':
            self.parsed_data['description'] = data