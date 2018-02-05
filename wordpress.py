"""Utilities to parse WordPress site data."""
import re
import scan
import logging
from message import msg

## TODO: add check for possible fatal errors (missing `</html>` tag).


def version(soup):
    """Find the WordPress version using the generator tag in the feed."""
    # TODO: Use hashes of public files if feed check fails https://github.com/philipjohn/exploit-scanner-hashes.
    # Use the official core checksum endpoint to build a list of unique hashes for publicly-accessible files?
    # https://api.wordpress.org/core/checksums/1.0/?version=3.6.1
    # https://github.com/wp-cli/checksum-command/blob/e7e6128e6a5115fea4c3e1e497c7ace2286f358d/src/Checksum_Core_Command.php#L217
    # TODO: Guess the feed URL if no link tags are found.
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

    Arguments:
        soup {BeautifulSoup}
        url {string}

    Returns:
        bool
    """
    wp_found_message = '✅ WordPress detected.'
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
    """Look for possible coming soon page.
    FIXME: Text like, “New products coming soon” produces false positives. Consider testing for low word count too?
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
    if html is None:
        logging.info('⚠️ No HTML content available.')
        return
    if '</html>' not in str(html):
        msg.send('⚠️ Closing HTML tag seems absent. Check logs for fatal errors?')


def parse_stylesheet_header(css):
    """Get WordPress theme data from CSS file contents via the comment header.

    Arguments:
        css {string} -- The contents of the CSS file.

    Returns:
        dict -- Theme info. See https://codex.wordpress.org/File_Header
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
