"""
A site diagnostic scanner for StudioPress support.

The StudioPress team often has to debug WordPress sites without admin access.
This tool accelerates the collection of data needed to solve support issues.
The information it gives is publicly available via browser dev tools or DNS.
"""
import scan
import spdns
import plugins
import wordpress
import themes

# TODO: Present a page showing a URL field.
# When the URL field is submitted, run the tests
# Or if a URL is passed via a GET param, automatically run the tests.
# Send results back over WebSockets? https://github.com/kennethreitz/flask-sockets

# TODO: put scans in /scans/ subdirectory with an __init__.py, then import scan.plugins, scan.dns, scan,wordpress, scan.themes

# TODO: look at multithreading HTTP requests: https://stackoverflow.com/a/2846697/88487

# URL = 'https://studiopress.com'
# URL = 'https://example.com'
URL = 'https://demo.studiopress.com/altitude/'

def main():
    """Scrape HTML from the URL and run tests."""
    print('Scanning ' + URL + '.')
    soup = scan.get(URL)

    print("\n===WordPress checks===")
    wordpress.is_wp(soup)
    wordpress.version(soup)
    wordpress.coming_soon_page(soup)

    print("\n===Theme checks===")
    if themes.is_genesis_child_theme(soup):
        print('✅ A Genesis child theme is active.')
    else:
        print('❌ A Genesis child theme was not found (or may be minified).')
        # TODO: best guess at the theme by grepping soup for 'themes/(.*)/'.
        # TODO: move these print lines into the functions like others.

    themes.print_theme_info(soup)
    themes.print_genesis_info(soup)

    print("\n===Plugin checks===")
    plugins.detect_plugins(soup)
    plugins.yoast(soup)
    plugins.caching(soup)

    print("\n===DNS checks===")
    spdns.points_to_sp_sites(URL)
    spdns.points_to_synthesis(URL)
    spdns.points_to_rainmaker(URL)
    spdns.uses_wordpress_dot_com(URL)
    spdns.uses_cloudflare(URL)


main()
