# University Data Scraper

This project is a web scraper built with Scrapy and Splash to collect university data from the YÖK Atlas website. It uses Scrapy for crawling and data extraction, and Splash for rendering and interacting with dynamic content loaded via Ajax.

## Overview

The scraper uses Scrapy in conjunction with Splash to handle JavaScript-rendered content and dynamically loaded pages. Splash allows the spider to interact with web pages by executing JavaScript, which is necessary for scraping data from pages that use Ajax to load content.

## Code Explanation

### `YokSpider` Class

The `YokSpider` class defines a Scrapy spider for scraping data from the YÖK Atlas website. Here’s a detailed explanation of the code:

#### 1. **Initialization**

- `name`: The name of the spider, used to identify it when running Scrapy commands.
- `counter`: A variable used to keep track of the number of pages processed.
- `start_urls`: A list containing the initial URL to start scraping from.

#### 2. **Lua Script**

The `script` variable contains a Lua script that is executed by Splash. This script handles the following tasks:

- **Disables Private Mode:** Ensures Splash does not use private browsing.
- **Sets Viewport Size:** Configures Splash to capture the full page.
- **Navigates to URL:** Loads the page specified by `args.url`.
- **Scrolls and Clicks:**
  - Uses JavaScript to scroll down the page and click the 'Next' button to load more data.
  - The script waits for the content to load before proceeding.
  - Continues this process based on the `page_number` argument, which controls how many times the 'Next' button is clicked.

- **Returns HTML:** Once the script completes, it returns the page's HTML and the current URL.

#### 3. **Start Requests**

- **`start_requests` Method:** Sends an initial request to the `start_urls` using `SplashRequest`.
  - **Arguments:**
    - `lua_source`: The Lua script to be executed by Splash.
    - `wait`: Time to wait for the page to load.
    - `page_number`: Current page number for handling pagination.
  - Increments the `counter` variable after sending the request to keep track of the number of pages processed.

#### 4. **Parsing Data**

- **`parse` Method:** Processes the response from Splash and extracts data.
  - **CSS Selectors:** Extracts data from specific columns of the table, such as `university_id`, `university_name`, `faculty_name`, etc.
  - **Yielding Items:** Creates a `UniversityItem` for each row and yields it to be processed by Scrapy’s pipeline.

- **Pagination Handling:**
  - **`next_page_url`:** Checks if there is a 'Next' button available.
  - **If a next page is available:** Sends a new `SplashRequest` for the next page and increments the `counter`.
  - **If no next page is available:** Logs a message indicating that there are no more pages to scrape.

## How It Works

1. **Initial Request:** The spider starts by sending a request to the initial URL using Splash, which renders the page and handles JavaScript.
2. **Dynamic Content Loading:** The Lua script interacts with the page, scrolling and clicking the 'Next' button to load additional data.
3. **Data Extraction:** The `parse` method extracts the data from the loaded page.
4. **Pagination:** The spider continues to scrape additional pages until no more pages are available.

## Requirements

- Python 3.x
- Scrapy
- Scrapy-Splash
- Splash server (running locally or on a remote server)

## Installation

1. Install the required Python packages:

   ```bash
   pip install scrapy scrapy-splash
    ```
2. Set up a Splash server. You can run it locally using Docker:
   ```bash
    docker run -p 8050:8050 scrapinghub/splash
   ```

3. Update the Scrapy project settings to include your Splash server URL:

   ```bash
   SPLASH_URL = 'http://localhost:8050'
   ```
4.Save the provided YokSpider code in a file named yok_spider.py within the spiders directory of your Scrapy project.

## Running the Spider
 ```bash
scrapy crawl yok_spider
   ```
## Discussion

- Scrapy is not suitable for modern dynamically loaded webpages if you can't acces to public API's of the webpage. For example https://yokatlas.yok.gov.tr/tercih-sihirbazi-t4-tablo.php?p=say has 100 pages at the same url and every page
has 50 universities. This url uses https://yokatlas.yok.gov.tr/server_side/server_processing-atlas2016-TS-t4.php API on the server side. Everytime user requested to the next page url remains same webpage POST requests to https://yokatlas.yok.gov.tr/server_side/server_processing-atlas2016-TS-t4.php
with form data at the payload part of the request.Clients can't acces this url with GET request webpage prints "Yetkisiz işlem" .I try to create fake POST request and fake header  with form data on nextbutton branch but failed.I think using selenium might be easier with this kind of pages

## Contact

This `README.md` file provides a comprehensive explanation of the Scrapy and Splash code, including how pagination is managed and the role of the counter variable.If you have any problems or solutions that i discussed contact me.





