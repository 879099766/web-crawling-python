# This file is responsible to extracting the domain so that we don't crawl useless domain
# Note: we only get the last two protocol domain word

from urllib.parse import urlparse


# get domain last two names (e.g., google.com)
def get_domain_name(url):
    try:
        # split the URL based on "."
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
        # Note: this will not work if the URL has something like ".co.za"
    except:
        return ''


# get sub domain name (e.g., mail.h-u-i.co.za)
def get_sub_domain_name(url):
    try:
        # parse the url and network location
        return urlparse(url).netloc
    except:
        return ''

# test:
# print(get_domain_name('https://nyit.edu/index.php'))
# print nyit.edu