# Steps:
# 1. spider gets a link in the waiting queue
# 2. spider crawls the link
# 3. stores the link that has been crawled so that we don't crawled again
# Note: we must design the sys to allow waiting queue and crawled list shareable amongst the multiple spiders

from urllib.request import urlopen
from link_finder import LinkFinder
from general import *


class Spider:

    # class variables in which they shared among all instances
    project_name = ''
    base_url = ''
    domain_name = ''
    # txt file
    queue_file = ''
    crawled_file = ''
    # waiting queue
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        # provide the shared info among the spiders
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name

        # set up the path
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'

        # start the web crawl. Note: when we run the first crawling, there's only one url in the waiting queue;
        # therefore, multiple threading will run once there are multiple url
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        # Note: we make the first spider to do a special job, which is to create prject file and txt docs
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)

        # now, converts the links in the data file to a set
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):

        # Make sure we don't crawl the page that has already been crawled
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))

            # "gather_links()" <-- connect to a web page and then return a set of all links that found on the page
            Spider.add_links_to_queue(Spider.gather_links(page_url))

            # remove the page that just crawled from the waiting queue and then add to the crawled list
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)

            # update the file
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        # gather links and return a set of links
        # Note: once we crawl the page, it will return bits (0 or 1); therefore, we need to convert to html

        html_string = ''

        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                # read the response as if it came from the ethernet cable
                html_bytes = response.read()

                # now decode the bytes that we receive by using UTF-8 encoding method so that we can get proper HTML
                html_string = html_bytes.decode("utf-8")

            # feed the page to the link finder to find all links
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)

        except:
            # handle error here
            print('Error: can not crawl page')
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        # add links that are already in the waiting queue
        # INPUT: set of links

        for url in links:
            # Pre-request:
            #     1. make sure they are not in the waiting list
            #     2. make sure they are in the crawled list so that we don't crawl it again
            #     3. make sure that we only crawl the domain that we want, not the other domains
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name not in url:
                continue

            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)




