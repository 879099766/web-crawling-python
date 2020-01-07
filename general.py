import os


# Each website you crawl is a separate project (folder)
def create_project_dir(directory):
    # check if a site has been crawled
    if not os.path.exists(directory):
        print("Creating projrcct " + directory)
        os.mkdir(directory)


# create queue and crawled files (if not created)
def create_data_files(project_name, base_url):
    # add url to the queue and wait to be crawl
    queue = project_name + "/queue.txt"
    # add url that has been crawled
    crawled = project_name + "/crawled.txt"

    # check if this file does exist
    if not os.path.isfile(queue):
        write_file(queue, base_url)

    if not os.path.isfile(crawled):
        # we create empty content
        write_file(crawled, '')


# create a new file
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


# para 1: project name; para 2: url to that website's home page
# create_data_files('thenewboston', 'https://thenewboston.com/')

# add data onto an existing file
def append_to_file(path, data):
    # "a" means append
    with open(path, 'a') as file:
        # jump to a new line for each data
        file.write(data + '\n')


# delete the contents of a file
def delete_fiile_contents(path):
    with open(path, 'w'):
        # do nothing
        pass


# read a file and convert each line to set items so that it will speed up the process
def file_to_set(file_name):
    result = set()
    # "rt" = read text file
    with open(file_name, 'rt') as f:
        for line in f:
            result.add(line.replace('\n', ''))
    return result


# iterate through a set, each item will be a new line in the file
def set_to_file(links, file):
    # delete old data coz the newer data is in links
    delete_fiile_contents(file)
    for link in sorted(links):
        append_to_file(file, link)
