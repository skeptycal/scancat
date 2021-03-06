"""Scan HTML content for active plugins."""
import re
import logging

from .message import msg


def detect_plugins(soup=None):
    """Output found plugins of interest.

    :param soup: The parsed HTML, defaults to None
    :type soup: BeautifulSoup, optional
    """
    if soup is None:
        logging.info('⚠️ No HTML content available.')
        return
    plugin_paths = [
        'agentpress-listings',
        'genesis-author-pro',
        'genesis-beta-tester',
        # 'genesis-connect-woocommerce',
        'woocommerce',
        '/jetpack/',
        'genesis-portfolio-pro',
        'genesis-responsive-slider',
        'genesis-simple-edits',
        'genesis-simple-faq',
        'genesis-simple-hooks',
        'genesis-simple-menus',
        'genesis-simple-share',
        'genesis-tabs',
        # 'seo-data-transporter',
        'simple-social-icons',
        # 'simple-urls',
        'social-profiles-widget',
    ]
    for path in plugin_paths:
        if(soup.find_all(string=re.compile(path))):
            msg.send('🔌 Found ' + path.replace('/', '') + '.')


def yoast(soup=None):
    """Output Yoast SEO detection status.

    :param soup: The parsed HTML, defaults to None
    :type soup: BeautifulSoup, optional
    """
    if soup is None:
        logging.info('⚠️ No HTML content available.')
        return
    is_yoast = soup.find_all(string=re.compile(
        'optimized with the Yoast SEO plugin'))
    if is_yoast:
        msg.send('🔌 Yoast SEO seems active.')
    else:
        msg.send('ℹ️ Yoast SEO not found.')


def caching(soup=None):
    """Output caching plugin strings found in HTML.

    :param soup: The parsed HTML, defaults to None
    :param soup: BeautifulSoup, optional
    """
    if soup is None:
        logging.info('⚠️ No HTML content available.')
        return
    cache_strings = {
        'Bluehost Endurance Cache': 'Generated by Endurance Page Cache',
        'W3 Total Cache': 'optimized by W3 Total Cache',
        'Comet Cache': 'Comet Cache is Fully Functional',
        'WP Fastest Cache': 'WP Fastest Cache',
    }
    for plugin_name, search_string in cache_strings.items():
        if(soup.find_all(string=re.compile(search_string))):
            msg.send(f"⚡ Found {plugin_name}.")
