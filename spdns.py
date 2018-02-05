import re
import dns.resolver
import scan
from message import msg


def guess_host(url):
    hosts = {
        'WordPress.com' : 'wordpress.com',
        'StudioPress Sites' : 'StudioPress Sites',
        'Rainmaker Platform' : 'Welcome to Rainmaker',
        'Synthesis Hosting' : 'Welcome to Synthesis',
        'Cloudflare' : 'Direct IP access not allowed',
        'WP Engine' : 'pointed at WP Engine',
    }
    soup, ip = get_page_at_domain_ip(url)
    host_found = None
    if soup:
        for host, search_text in hosts.items():
            host_found = soup.find_all(string=re.compile(search_text))
            if host_found:
                msg.send('ℹ️ A record points to ' + host + '. [' + ip + ']')
                return
    if not host_found and ip:
        msg.send('ℹ️ A record points to ' + ip + '. Unknown host.')


def get_page_at_domain_ip(url):
    """Given a URL, loop through A record IPs and return HTML from first that loads.

    Server default pages often given info about the web host who runs them.
    """
    url = scan.clean_url(url)
    try:
        answers = dns.resolver.query(url, 'A')
        soup = None
        for rdata in answers:
            ip = rdata.to_text()
            soup = scan.get('http://' + ip)
            if soup is None:
                continue
        return soup, ip
    except dns.resolver.NoNameservers:
        msg.send('Nameserver not reachable (SERVFAIL) for ' + url + '.', log=True)
        return None, None
    except dns.resolver.NXDOMAIN:
        msg.send('DNS query failed (local, test, or bad domain?): ' + url, log=True)
        return None, None


def uses_cloudflare(url):
    """Do NS records point to Cloudflare?"""
    # TODO: Include check for private CF nameservers. HEAD and grep for CF headers?
    url = scan.clean_url(url)
    try:
        answers = dns.resolver.query(url, 'NS')
        for rdata in answers:
            if 'cloudflare' in rdata.to_text():
                msg.send('ℹ️ Using Cloudflare ' + '[NS: ' + rdata.to_text() + ']')
                return
        msg.send('ℹ️ Not using shared Cloudflare nameservers.')
    except dns.resolver.NoAnswer:
        msg.send('No NS record for ' + url + '.')
    except dns.resolver.NXDOMAIN:
        msg.send('DNS query failed (local, test, or bad domain?): ' + url)


def has_mail(url):
    """If the domain has MX records configured, what are they?"""
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
