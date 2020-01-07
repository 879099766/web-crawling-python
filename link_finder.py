# paring html by using python build-in class
# steps:
# 1. create a link finder obj
# 2. feed in html of the target page
# 3. once found the target pages, then run "page_links"

from html.parser import HTMLParser
from urllib import parse


class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        # base_url is the domain of the site
        self.base_url = base_url
        self.page_url = page_url
        # store crawled links in a set
        self.links = set()

    def handle_starttag(self, tag, attrs):
        # override the default method
        # print(tag)
        if tag == 'a':
            # if this tag is <a>
            for (attribute, value) in attrs:
                if attribute == 'href':
                    # we only care about the href attribute of <a> tag
                    # NOTE: we ignore the relative href URL because we need full URL path of the source with domain name
                    url = parse.urljoin(self.base_url, value)
                    # this joins the base url to the value of the source
                    # Note, if the source already has base url in their source, then this automatically join the base
                    self.links.add(url)

    def page_links(self):
        return self.links

    def error(self, message):
        # error goes here
        pass

# finder = LinkFinder()
# feed the html tags
# finder.feed('<html><head><title>Test</title></head><body><h1>Parse me!</h1></body></html>')
