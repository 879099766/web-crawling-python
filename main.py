# driver of the web crawler in multi threads

import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'skymoble'
HOMEPAGE = 'https://skymobile.us/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8

# thread queue
queue = Queue()

# define a spider
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# create work threads
# Note: it will be terminated when main exits
def create_workers():
    # aka, create threads
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)

        # make the thread run in daemon process and die whenever the main exists
        t.daemon = True
        t.start()


# do the next job in the waiting queue
def work():
    while True:
        # make the each spider to grab the url inside the queue.txt
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# each queued link is a new job
def create_jobs():
    # this will be called as long as the link(s) needs to be crawl
    for link in file_to_set(QUEUE_FILE):
        # store the data inside queue.txt to thread queue
        queue.put(link)

    # make sure the thread to get its turn to run so that to avoid thread lock
    queue.join()
    crawl()


# check if there are items in the waiting queue, if so crawl them
def crawl():
    # working with set
    queued_links = file_to_set(QUEUE_FILE)

    if len(queued_links) > 0:
        # make sure we are crawling things that are available
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

# run the application
create_workers()
crawl()