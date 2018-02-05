import re
import dns.resolver
import scan
from message import msg

# TODO: Refactor into two functions — a DNS lookup, and a search for a string at that IP.
def points_to_sp_sites(url):
    """Do 'A' records point to StudioPress Sites hosting?

    Visit the page at the A record's IP and look for StudioPress
    Sites -specific default text.

    Arguments:
        url {string} -- The URL in any valid format.
    """
    url = scan.clean_url(url)
    try:
        answers = dns.resolver.query(url, 'A')
        for rdata in answers:
            ip_as_url = 'http://' + rdata.to_text()
            soup = scan.get(ip_as_url)
            if soup is None:
                continue
            is_sp_sites = soup.find_all(string=re.compile('StudioPress Sites'))
            if is_sp_sites:
                msg.send('✅ Hosted with StudioPress Sites ' +
                      '[IP: ' + ip_as_url + '].')
                return
        msg.send('❌ A records not pointed to StudioPress Sites.')
    except dns.resolver.NoNameservers:
        msg.send('Nameserver not reachable (SERVFAIL) for ' + url + '.')
    except dns.resolver.NXDOMAIN:
        msg.send('DNS query names do not exist (local or test domain?).')


def points_to_synthesis(url):
    """Do A records points to Synthesis hosting?"""
    url = scan.clean_url(url)
    try:
        answers = dns.resolver.query(url, 'A')
        for rdata in answers:
            ip_as_url = 'http://' + rdata.to_text()
            soup = scan.get(ip_as_url)
            if soup is None:
                continue
            is_synthesis = soup.find_all(
                string=re.compile('Welcome to Synthesis'))
            if is_synthesis:
                msg.send('✅ Hosted with Synthesis ' + '[IP: ' + ip_as_url + '].')
                return
        msg.send('❌ A records not pointed to Synthesis.')
    except dns.resolver.NoNameservers:
        msg.send('Nameserver not reachable (SERVFAIL) for ' + url + '.')
    except dns.resolver.NXDOMAIN:
        msg.send('DNS query names do not exist (local or test domain?).')


def points_to_rainmaker(url):
    """Is the site hosted on the Rainmaker Platform?"""
    url = scan.clean_url(url)
    try:
        answers = dns.resolver.query(url, 'A')
        for rdata in answers:
            ip_as_url = 'http://' + rdata.to_text()
            soup = scan.get(ip_as_url)
            if soup is None:
                continue
            is_rainmaker = soup.find_all(
                string=re.compile('Welcome to Rainmaker'))
            if is_rainmaker:
                msg.send('✅ Hosted with Rainmaker ' + '[IP: ' + ip_as_url + '].')
                return
        msg.send('❌ A records not pointed to Rainmaker.')
    except dns.resolver.NoNameservers:
        msg.send('Nameserver not reachable (SERVFAIL) for ' + url + '.')
    except dns.resolver.NXDOMAIN:
        msg.send('DNS query names do not exist (local or test domain?).')


def uses_cloudflare(url):
    """Do NS records point to Cloudflare?"""
    # TODO: Include check for private CF nameservers. HEAD and grep for CF headers?
    url = scan.clean_url(url)
    try:
        answers = dns.resolver.query(url, 'NS')
        for rdata in answers:
            if 'cloudflare' in rdata.to_text():
                msg.send('✅ Using Cloudflare ' + '[NS: ' + rdata.to_text() + ']')
                return
        msg.send('❌ Nameservers don’t appear to be Cloudflare’s.')
    except dns.resolver.NoAnswer:
        msg.send('No NS record for ' + url + '.')
    except dns.resolver.NXDOMAIN:
        msg.send('DNS query names do not exist (local or test domain?).')


def uses_wordpress_dot_com(url):
    """Check if the site is using WP.com instead of a self-hosted install."""
    url = scan.clean_url(url)
    try:
        answers = dns.resolver.query(url, 'A')
        for rdata in answers:
            ip_as_url = 'http://' + rdata.to_text()
            soup = scan.get(ip_as_url)
            if soup is None:
                continue
            is_wp_com = soup.find_all(string=re.compile('wordpress.com'))
            if is_wp_com:
                msg.send('✅ Hosted with WordPress.com ' + '[IP: ' + ip_as_url + '].')
                return
        msg.send('❌ A records not pointed to WordPress.com.')
    except dns.resolver.NoNameservers:
        msg.send('Nameserver not reachable (SERVFAIL) for ' + url + '.')
    except dns.resolver.NXDOMAIN:
        msg.send('DNS query names do not exist (local or test domain?).')

# TODO: Abstract the above into a general method that checks for strings.
# TODO: Check A record IP page for presence of 'Direct IP access not allowed',
# which indicates a Cloudflare page.


def has_mail():
    """If the domain has MX records configured, what are they?"""
    pass
