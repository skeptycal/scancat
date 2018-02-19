"""Utilities to parse WordPress site data."""
import re
import logging

from . import scan
from .message import msg


def version(soup):
    """Output the WordPress version using the generator tag in the feed.

    :param soup: The parsed HTML
    :type soup: BeautifulSoup
    """
    if soup is None:
        logging.info('⚠️ No HTML content available.')
        return
    feed_tags = soup.findAll('link', attrs={'type':'application/rss+xml'})
    feed_urls = [tag["href"] for tag in feed_tags]
    if not feed_urls:
        msg.send('WordPress version could not be guessed (no feed URL found).')
        return
    for url in feed_urls:
        soup, _ = scan.get(url)
        if soup is None:
            continue
        generator_tag = soup.find('generator')
        if generator_tag:
            wp_version_text = generator_tag.getText().split('v=')
            if len(wp_version_text) > 1:
                wp_version = wp_version_text[1]
                msg.send('WordPress version: ' + wp_version + '.')
                return


def is_wp(soup=None, url=None):
    """Is this a WordPress site?

    :param soup: The parsed HTML, defaults to None
    :type soup: BeautifulSoup, optional
    :param url: Site URL, defaults to None
    :type url: string, optional
    :rtype: bool
    """
    wp_found_message = '👃 Smells like WordPress.'
    if url is None and soup is None:
        msg.send('No HTML or URL provided.')
        return False
    if url and not soup:
        soup, _ = scan.get(url)
    has_wp_content = soup.find_all(string=re.compile('/wp-content/'))
    if has_wp_content:
        msg.send(wp_found_message)
        return True


def coming_soon_page(soup):
    """Output a message if a coming soon page is detected.
    FIXME: Text like, “New products coming soon” produces false positives. Consider checking for low word count too?

    :param soup: The parsed HTML
    :type soup: BeautifulSoup
    """
    if soup is None:
        logging.info('⚠️ No HTML content available.')
        return
    coming_soon_strings = [
        'coming soon',
        'maintenance mode'
    ]
    for string in coming_soon_strings:
        if soup.find_all(string=re.compile(string, re.IGNORECASE)):
            msg.send('⚠️ Possible maintenance mode text: ' + '“' + string + '”')
            return


def html_end_tag_missing(html):
    """Warn if raw HTML omits </html>, which suggests a fatal error.

    :param html: The unparsed HTML
    :type html: string
    """
    if html is None:
        logging.info('⚠️ No HTML content available.')
        return
    if '</html>' not in str(html):
        msg.send('⚠️ Closing HTML tag seems absent. Check PHP logs for fatal errors?')


def parse_stylesheet_header(css):
    """Get WordPress theme data from CSS file contents via the comment header.

    :param css: The contents of the CSS file
    :type css: string
    :return: Theme info. See https://codex.wordpress.org/File_Header
    :rtype: dict
    """
    headers = [
        'Theme Name',
        'Theme URI',
        'Description',
        'Author',
        'Author URI',
        'Version',
        'Template',
        'Template Version',
        'Status',
        'Tags',
        'Text Domain',
        'Domain Path'
    ]
    result = {}
    for header in headers:
        regex = re.escape(header + ':') + r'(.*)'
        match = re.search(regex, css, flags=re.IGNORECASE)
        if match:
            result[header.lower().replace(' ', '_')] = match.group(1).strip()
    return result
