import re

import dns.resolver

from . import scan
from .message import msg


def guess_host(url):
    """Guess the host by scraping the HTML page at the domain's A record IP.

    :param url: The site address
    :type url: string
    """

    hosts = {
        'Amazon S3': 'Amazon S3',
        'Cloudflare': 'Direct IP access not allowed',
        'Heroku': 'herokucdn.com',
        'InMotion Hosting': 'inmotionhosting.com',
        'SiteGround': 'provided by SiteGround.com',
        'StudioPress Sites': 'StudioPress Sites',
        'Synthesis Hosting': 'Welcome to Synthesis',
        'The Rainmaker Platform': 'Welcome to Rainmaker',
        'WordPress.com': 'wordpress.com',
        'WP Engine': 'pointed at WP Engine',
    }
    html, ip = get_page_at_domain_ip(url)
    host_found = None
    if html:
        for host, search_text in hosts.items():
            if search_text in str(html):
                msg.send('ℹ️ A record points to ' + host + '. [' + ip + ']')
                return
    if not host_found and ip:
        msg.send('ℹ️ A record points to ' + ip + '. Unknown host.')


def get_page_at_domain_ip(url):
    """Return HTML from first A record IP address that loads.

    :param url: The site address
    :type url: string
    :return: Tuple of raw HTML and IP
    :rtype: string, string or None, None
    """
    url = scan.clean_url(url)
    try:
        answers = dns.resolver.query(url, 'A')
        soup = None
        for rdata in answers:
            ip = rdata.to_text()
            _, raw_html = scan.get('http://' + ip, raise_for_status=False)
            if raw_html is None:
                continue
        return raw_html, ip
    except dns.resolver.NoNameservers:
        msg.send('Nameserver not reachable (SERVFAIL) for ' +
                 url + '.', log=True)
        return None, None
    except dns.resolver.NXDOMAIN:
        msg.send('DNS query failed (local, test, or bad domain?): ' + url, log=True)
        return None, None


def uses_cloudflare(url):
    """Output message if NS records point to Cloudflare.

    :param url: The site address
    :type url: string
    """
    url = scan.clean_url(url)
    try:
        answers = dns.resolver.query(url, 'NS')
        for rdata in answers:
            if 'cloudflare' in rdata.to_text():
                msg.send('🌩️ Using Cloudflare ' +
                         '[NS: ' + rdata.to_text() + ']')
                return
        msg.send('ℹ️ Not using shared Cloudflare nameservers.')
    except dns.resolver.NoAnswer:
        msg.send('No NS record for ' + url + '.')
    except dns.resolver.NXDOMAIN:
        msg.send('DNS query failed (local, test, or bad domain?): ' + url)


def has_mail(url):
    """Output first MX record found if available.

    :param url: The site address
    :type url: string
    """
    url = scan.clean_url(url)
    try:
        answers = dns.resolver.query(url, 'MX')
        for rdata in answers:
            msg.send('ℹ️ Found MX record: ' + rdata.to_text())
            return
        msg.send('ℹ️ No MX records found for ' + url + '.')
    except dns.resolver.NoAnswer:
        msg.send('No MX record for ' + url + '.')
    except dns.resolver.NXDOMAIN:
        msg.send('DNS query failed (local, test, or bad domain?): ' + url)
