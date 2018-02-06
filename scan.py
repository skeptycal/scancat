"""
Scan gives diagnostic info about a site at a given URL. Tests are specific to
WordPress sites and StudioPress themes and plugins.
"""
import re
import logging
from urllib.parse import urlsplit
import requests
from bs4 import BeautifulSoup
import validators
from message import msg


def get(url):
    """Fetch HTML from the URL."""
    if not re.match(r'http(s?)\:', url):
        url = 'http://' + url
    if not validators.url(url):
        msg.send('⚠️ URL seems invalid: ' + url)
        logging.info('⚠️ URL invalid: ' + url)
        return None, None
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        html = requests.get(url, headers=headers)
        html.raise_for_status()
        return BeautifulSoup(html.content, 'html.parser'), html.content
    except requests.HTTPError:
        logging.info('⚠️ Error: ' + str(html.status_code) +
              ' code returned from ' + url + '.')
        return None, None
    except requests.ConnectionError as error:
        logging.info('⚠️ Error: Could not connect. ' + str(error))
        return None, None


def clean_url(url):
    """Strip protocol and path from the URL leaving the domain name."""
    if not re.match(r'http(s?)\:', url):
        url = 'http://' + url
    url_parts = urlsplit(url)
    return url_parts.netloc
