"""
A site diagnostic scanner for StudioPress support.

The StudioPress team often has to debug WordPress sites without admin access.
This tool accelerates the collection of data needed to solve support issues.
The information it gives is publicly available via browser dev tools or DNS.
"""
import sys
import logging

from message import msg
import scan
import spdns
import plugins
import wordpress
import themes
from flask import Flask
from flask_sockets import Sockets

# TODO: put scans in /scans/ subdirectory with an __init__.py, then import scan.plugins, scan.dns, scan,wordpress, scan.themes
# TODO: look at multithreading HTTP requests: https://stackoverflow.com/a/2846697/88487
def start_scan(url, ws=None):
    """Scrape HTML from the URL and run tests."""
    logging.basicConfig(level=logging.INFO)
    msg.websocket = ws
    msg.send('Scanning ' + url + '.')
    soup = scan.get(url)

    msg.title('WordPress checks')
    wordpress.is_wp(soup)
    wordpress.version(soup)
    wordpress.coming_soon_page(soup)

    msg.title('Theme checks')
    if themes.is_genesis_child_theme(soup):
        msg.send('✅ A Genesis child theme is active.')
    else:
        msg.send('❌ A Genesis child theme was not found (or may be minified).')
        # TODO: best guess at the theme by grepping soup for 'themes/(.*)/'.
        # TODO: move these print lines into the functions like others.

    themes.print_theme_info(soup)
    themes.print_genesis_info(soup)

    msg.title('Plugin checks')
    plugins.detect_plugins(soup)
    plugins.yoast(soup)
    plugins.caching(soup)

    msg.title('DNS checks')
    spdns.points_to_sp_sites(url)
    spdns.points_to_synthesis(url)
    spdns.points_to_rainmaker(url)
    spdns.uses_wordpress_dot_com(url)
    spdns.uses_cloudflare(url)


app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        URL = ws.receive()
        if URL:
            start_scan(URL, ws)


@app.route('/')
def root():
    return app.send_static_file('home.html')


"""Run via command line using first arg as URL."""
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_scan(sys.argv[1])
