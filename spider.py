# import necessary modules
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# create a lock object to synchronize access to shared resources in a multi-threaded environment
lock = threading.Lock()

# define a function that takes a URL as input, fetches the HTML content using requests, parses it using BeautifulSoup, 
# extracts all links from the page and returns a dictionary object with the URL, title and content of the page, 
# and a list of links on the page
def crawl_url(url):
    with requests.Session() as session:
        try:
            response = session.get(url)
        except requests.exceptions.RequestException as e:
            print(f"Error while fetching {url}: {e}")
            return None

        soup = BeautifulSoup(response.content, 'html5lib')

        # check if the URL points to a PDF file
        is_pdf = urlparse(url).path.lower().endswith('.pdf')
        data = {
            'url': url,
            'title': soup.title.string.strip() if soup.title else '',
            'content': '' if is_pdf else ' '.join(soup.stripped_strings)
        }

        # if the URL points to a PDF file, log it in a file called skipped.log
        if is_pdf:
            with lock, open('skipped.log', 'a') as f:
                f.write(f"Skipped: {url}\n")

        # extract all links from the page and convert them to absolute URLs using the urljoin function
        # filter out some types of URLs (such as those that start with #, javascript:, tel:, mailto:, and Mailto:)
        links = [urljoin(url, link['href']) for link in soup.find_all('a', href=True) if not (link['href'].startswith(('#', 'javascript:', 'tel:', 'mailto:', 'Mailto:')))]

    return data, links

# define a function that takes a start URL and a max_workers parameter, 
# initializes a set to track visited links and a deque to store URLs to crawl,
# creates a thread pool using ThreadPoolExecutor with a maximum number of workers,
# fetches the data for each URL and its associated links, and writes the data to a JSON file called website_data.json
def crawl_website(start_url, max_workers=10):
    visited_links = set()
    url_queue = deque([start_url])

    def write_data(data):
        with lock, open('website_data.json', 'a') as f:
            json.dump(data, f)
            f.write('\n')

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while url_queue:
            # submit each URL in the URL queue to the thread pool and store the future object and the corresponding URL in a dictionary
            future_to_url = {executor.submit(crawl_url, url): url for url in url_queue}
            url_queue.clear()

            for future in as_completed(future_to_url):
                # extract the URL from the dictionary using the future object
                url = future_to_url[future]
                # add the URL to the set of visited links
                visited_links.add(url)

                try:
                    # get the result of the future object
                    result = future.result()
                except Exception as exc:
                    print(f"{url} generated an exception: {exc}")
                else:
                    if result is not None:
                        # extract the data and links from the result
                        data, links = result
                        # write the data to the JSON file
                        write_data(data)

                        # add any new links to the URL queue
                        for link in links:
                            if link not in visited_links:
                                url_queue.append(link)

# The code block is an entry point to the script that checks if the script is being run as the main program. 
# If the script is being run as the main program, it sets a variable `start_url` to 'http://example.com'.
# Finally, the `crawl_website` function is called with the `start_url` as its parameter to initiate the crawling process.

if __name__ == '__main__':
    start_url = 'http://example.com'
    crawl_website(start_url)
