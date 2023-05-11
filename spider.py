import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

lock = threading.Lock()

def crawl_url(url):
    with requests.Session() as session:
        try:
            response = session.get(url)
        except requests.exceptions.RequestException as e:
            print(f"Error while fetching {url}: {e}")
            return None

        soup = BeautifulSoup(response.content, 'html5lib')

        is_pdf = urlparse(url).path.lower().endswith('.pdf')
        data = {
            'url': url,
            'title': soup.title.string.strip() if soup.title else '',
            'content': '' if is_pdf else ' '.join(soup.stripped_strings)
        }

        if is_pdf:
            with lock, open('skipped.log', 'a') as f:
                f.write(f"Skipped: {url}\n")

        links = [urljoin(url, link['href']) for link in soup.find_all('a', href=True) if not (link['href'].startswith(('#', 'javascript:', 'tel:', 'mailto:', 'Mailto:')))]

    return data, links

def crawl_website(start_url, max_workers=10):
    visited_links = set()
    url_queue = deque([start_url])

    def write_data(data):
        with lock, open('website_data.json', 'a') as f:
            json.dump(data, f)
            f.write(',')

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while url_queue:
            future_to_url = {executor.submit(crawl_url, url): url for url in url_queue}
            url_queue.clear()

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                visited_links.add(url)

                try:
                    result = future.result()
                except Exception as exc:
                    print(f"{url} generated an exception: {exc}")
                else:
                    if result is not None:
                        data, links = result
                        write_data(data)

                        for link in links:
                            if link not in visited_links:
                                url_queue.append(link)

    with open('website_data.json', 'a') as f:
        f.write(']') # Add a "]" to signify end of JSON array


if __name__ == '__main__':
    start_url = 'http://dee.ne.gov'
    crawl_website(start_url)
