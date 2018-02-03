"""Probe a WordPress site for theme information."""
import wordpress as wp
import requests
from bs4 import BeautifulSoup


def is_genesis_child_theme(soup=None):
    """Is the active theme a Genesis child theme?"""
    if soup is None:
        print('⚠️ Error: No HTML content available.')
        return
    info, _ = theme_info(soup)
    if info is None:
        return False
    if 'template' in info and info['template'].lower() == 'genesis':
        return True
    return False


def print_genesis_info(soup=None):
    """Get Genesis parent theme version info if it can be found.

    Keyword Arguments:
        soup {BeautifulSoup} (default: {None})

    Returns:
        string -- Genesis info or empty string.
    """
    if soup is None:
        print('⚠️ Error: No HTML content available.')
        return
    _, child_theme_style_url = theme_info(soup)
    if child_theme_style_url:
        genesis_style_url = child_theme_style_url.split(
            '/wp-content/', 1)[0] + '/wp-content/themes/genesis/style.css'
        genesis_theme_info, url = theme_info(None, [genesis_style_url])
        if genesis_theme_info and url:
            print('- Genesis version: ' +
                  genesis_theme_info['version'] + ' [' + url + ']')


def stylesheets(soup=None):
    """Find stylesheet URLs in HTML code.

    Keyword Arguments:
        soup {BeautifulSoup} (default: {None})

    Returns:
        list -- All stylesheet URLs from link tags.
    """
    if soup is None:
        print('⚠️ Error: No HTML content available.')
        return
    links = soup.findAll('link', attrs={'rel': 'stylesheet'})
    stylesheet_urls = [link["href"] for link in links]
    return stylesheet_urls


def theme_info(soup=None, theme_stylesheet_urls=None):
    """Get active theme information."""
    if soup is None and theme_stylesheet_urls is None:
        print('⚠️ Error: No HTML content available.')
        return None, None
    if theme_stylesheet_urls is None:
        stylesheet_urls = stylesheets(soup)
        theme_stylesheet_urls = list(
            filter(lambda url: '/themes/' in url, stylesheet_urls))
    for url in theme_stylesheet_urls:
        css = requests.get(url)
        info = wp.parse_stylesheet_header(css.text)
        if 'theme_name' in info:
            return info, url
    return None, None


def print_theme_info(soup=None):
    """Print active theme information."""
    not_found_message = 'No theme info found. Styles may be minified, in an unexpected place, behind a maintenance mode page, or the site is not using WordPress.'
    if soup is None:
        print('⚠️ Error: No HTML content available.')
        return
    info, url = theme_info(soup)
    if info is None:
        print(not_found_message)
        return
    if 'theme_name' in info:
        print('- Theme name: ' + info['theme_name'])
    else:
        print(not_found_message)

    if 'version' in info:
        print('- Version: ' + info['version'] + ' [' + url + ']')