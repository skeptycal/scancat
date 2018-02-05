"""
Scan gives diagnostic info about a site at a given URL. Tests are specific to
WordPress sites and StudioPress themes and plugins.
"""
import re
import logging
from urllib.parse import urlsplit
import requests
from bs4 import BeautifulSoup
from message import msg


def get(url):
    """Fetch HTML from the URL."""
    if not re.match(r'http(s?)\:', url):
        url = 'http://' + url
    try:
        html = requests.get(url)
        html.raise_for_status()
        return BeautifulSoup(html.content, 'html.parser')
    except requests.HTTPError:
        logging.info('⚠️ Error: ' + str(html.status_code) +
              ' code returned from ' + url + '.')
    except requests.ConnectionError as error:
        logging.info('⚠️ Error: Could not connect. ' + str(error))


def clean_url(url):
    """Strip protocol and path from the URL leaving the domain name."""
    if not re.match(r'http(s?)\:', url):
        url = 'http://' + url
    url_parts = urlsplit(url)
    return url_parts.netloc
