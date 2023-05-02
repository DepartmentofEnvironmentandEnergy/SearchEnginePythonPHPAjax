# Search Engine Python, PHP, AJAX

# Author: Austen Green of AustenJGreen.com


This script is a simple web crawler that starts from a given URL and crawls the website to collect data on each page, skipping any PDF files. The collected data is saved to a JSON file, and the URLs of skipped PDFs are logged in a separate file.

## Prerequisites

To run this script, you need to have Python 3 installed on your system. The script also requires the following Python libraries:

- `requests`
- `bs4`
- `html5lib`

You can install them using `pip` by running:

```
pip install requests beautifulsoup4 html5lib
```

## How to run the script

1. Save the code provided above to a file named `web_crawler.py` in your desired directory.
2. Open a terminal and navigate to the directory where the `web_crawler.py` file is located.
3. Before running the script, edit the `start_url` variable in the `__main__` block at the bottom of the script to the URL you want to start crawling. For example:

   ```python
   start_url = 'http://example.com'
   ```

4. Run the script with the following command:

   ```
   python spider.py
   ```

5. The script will crawl the specified website and collect data on each page. The collected data will be saved in a file named `website_data.json`, and the URLs of any skipped PDF files will be logged in a file named `skipped.log`.

## Customization

You can adjust the number of concurrent workers (threads) used by the crawler by modifying the `max_workers` parameter in the `crawl_website` function call. The default value is 10. For example, to use 20 workers:

```python
crawl_website(start_url, max_workers=20)
```

Please note that increasing the number of workers may put more stress on the target website and your system, so adjust it with caution.
