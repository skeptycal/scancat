"""
A site diagnostic scanner.

This tool accelerates the collection of data needed to solve support issues
with websites. The information it gives is publicly available via browser
developer tools and DNS.
"""
import os
import sys
import logging
import random

from flask import Flask, render_template
from flask_sockets import Sockets
from flask_sslify import SSLify

from scancat import plugins, scan, spdns, themes, wordpress
from scancat.message import msg


app = Flask(__name__)
sockets = Sockets(app)
sslify = SSLify(app)


app.debug = True
if 'PRODUCTION' in os.environ:
    app.debug = False


@app.route('/')
def root():
    cats = [
        'acrobat',
        'banjo',
        'drink',
        'facepalm',
        'fly',
        'gift',
        'knead',
        'love',
        'meal',
        'popcorn',
        'purr',
        'sleepy',
        'walk',
    ]
    return render_template('home.html', cat=random.choice(cats))


@app.route('/about/')
def about():
    return render_template('about.html')


@sockets.route('/scan')
def echo_socket(ws):
    while not ws.closed:
        URL = ws.receive()
        if URL:
            start_scan(URL, ws)


def start_scan(url, ws=None):
    """Scrape HTML from the URL and run tests."""
    logging.basicConfig(level=logging.INFO)
    msg.websocket = ws
    url = url.strip()
    msg.send(f"🔍 Sniffing {url}.", log=True)
    soup, raw_html = scan.get(url)

    wp = wordpress.is_wp(soup)

    if wp:
        msg.title('WordPress')
        wordpress.version(soup)
        wordpress.coming_soon_page(soup)
        wordpress.html_end_tag_missing(raw_html)
        msg.title('Themes', level=3)
        themes.is_genesis_child_theme(soup)
        themes.print_theme_info(soup)
        themes.print_genesis_info(soup)
        msg.title('Plugins', level=3)
        plugins.detect_plugins(soup)
        plugins.yoast(soup)
        plugins.caching(soup)

    msg.title('DNS')
    spdns.guess_host(url)
    spdns.uses_cloudflare(url)
    spdns.has_mail(url)

    msg.send('🏁 Scan complete.')

    if ws:
        ws.close()


"""Run via command line using first arg as URL."""
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_scan(sys.argv[1])
