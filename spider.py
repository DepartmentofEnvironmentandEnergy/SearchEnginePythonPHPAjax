# import json
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin

# def crawl_website(start_url):
#     visited_links = set()
#     data = []

#     def crawl(url):
#         if url in visited_links:
#             return

#         response = requests.get(url)
#         soup = BeautifulSoup(response.content, 'html5lib')  # Updated parser
#         visited_links.add(url)

#         for link in soup.find_all('a'):
#             href = link.get('href')
#             if href and not href.startswith('#') and not href.startswith('javascript:') and not href.startswith('tel:') and not href.startswith('mailto:') and not href.startswith('Mailto:'):
#                 full_url = urljoin(url, href)
#                 crawl(full_url)

#         data.append({
#             'url': url,
#             'title': soup.title.string.strip() if soup.title else '',
#             'content': ' '.join(soup.stripped_strings)
#         })

#     crawl(start_url)

#     with open('website_data.json', 'w') as f:
#         json.dump(data, f)

# if __name__ == '__main__':
#     start_url = 'http://dee.ne.gov'  # Replace with the URL you want to crawl
#     crawl_website(start_url)



# Optimized code no memory saving

# import json
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# from collections import deque

# def crawl_website(start_url):
#     visited_links = set()
#     data = []  # This list will store the data for each URL
#     session = requests.Session()
#     url_queue = deque([start_url])

#     while url_queue:
#         url = url_queue.popleft()

#         if url in visited_links:
#             continue

#         try:
#             response = session.get(url)
#         except requests.exceptions.RequestException as e:
#             print(f"Error while fetching {url}: {e}")
#             continue

#         soup = BeautifulSoup(response.content, 'html5lib')
#         visited_links.add(url)

#         for link in soup.find_all('a', href=True):
#             href = link['href']
#             if not (href.startswith('#') or href.startswith('javascript:') or href.startswith('tel:') or href.startswith('mailto:') or href.startswith('Mailto:')):
#                 full_url = urljoin(url, href)
#                 if full_url not in visited_links:
#                     url_queue.append(full_url)

#         # This block appends the data for the current URL to the 'data' list
#         data.append({
#             'url': url,
#             'title': soup.title.string.strip() if soup.title else '',
#             'content': ' '.join(soup.stripped_strings)
#         })

#     # After the while loop is done, the 'data' list is written to the 'website_data.json' file
#     with open('website_data.json', 'w') as f:
#         json.dump(data, f)

# if __name__ == '__main__':
#     start_url = 'http://dee.ne.gov'  # Replace with the URL you want to crawl
#     crawl_website(start_url)



# # Append each iteration to file to save memory for overall operation
# import json
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# from collections import deque

# def crawl_website(start_url):
#     visited_links = set()
#     session = requests.Session()
#     url_queue = deque([start_url])

#     # This function writes the data to the JSON file
#     def write_data(data):
#         with open('website_data.json', 'a') as f:
#             json.dump(data, f)
#             f.write('\n')  # Add a newline after each JSON object

#     while url_queue:
#         url = url_queue.popleft()

#         if url in visited_links:
#             continue

#         try:
#             response = session.get(url)
#         except requests.exceptions.RequestException as e:
#             print(f"Error while fetching {url}: {e}")
#             continue

#         soup = BeautifulSoup(response.content, 'html5lib')
#         visited_links.add(url)

#         for link in soup.find_all('a', href=True):
#             href = link['href']
#             if not (href.startswith('#') or href.startswith('javascript:') or href.startswith('tel:') or href.startswith('mailto:') or href.startswith('Mailto:')):
#                 full_url = urljoin(url, href)
#                 if full_url not in visited_links:
#                     url_queue.append(full_url)

#         # This block creates the data object for the current URL
#         data = {
#             'url': url,
#             'title': soup.title.string.strip() if soup.title else '',
#             'content': ' '.join(soup.stripped_strings)
#         }

#         # Call the write_data function to append the data to the JSON file
#         write_data(data)

# if __name__ == '__main__':
#     start_url = 'http://dee.ne.gov'  # Replace with the URL you want to crawl
#     crawl_website(start_url)


# Thread Locking / Enabling more threads to make it process faster
#   This implementation uses a thread pool with a default of 10 worker threads to crawl websites concurrently. 
#   You can adjust the max_workers parameter to change the number of threads used. 
#   Keep in mind that increasing the number of threads will also increase the load on your system and the target website.

