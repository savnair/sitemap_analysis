import sys
import scrapy
import os
from scrapy.spiders import CrawlSpider
from urllib.parse import urlparse

class CrawlSpider(CrawlSpider):
    name = 'crawl_spider'
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15'
    #custom_settings = {'DEPTH_LIMIT': 100}

    def __init__(self, *args, **kwargs):
        super(CrawlSpider, self).__init__(*args, **kwargs)
        self.seen_domains = set()

    def start_requests(self):
        start_urls = ['https://www.wikipedia.org',
                      'https://www.google.com/search?q=food',
                      'https://www.cnn.com']

        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # Extract domain names from the current page
        domain_names = set()
        max_file_size_bytes = 1024 * 1024  # Set the maximum file size to 1 MB
        file_path = '/Users/savitha/mycrawler/domain_names1.txt'

        for link in response.css('a::attr(href)').extract():
            parsed_url = urlparse(link)
            if parsed_url.netloc:
                domain_names.add(parsed_url.netloc)

        # Write domain names to a local file
        with open('domain_names1.txt', 'a') as f:
            for domain in domain_names:
                if domain not in self.seen_domains:
                    f.write(domain + '\n')
                    self.seen_domains.add(domain)

                    if os.path.getsize(file_path) > max_file_size_bytes:
                        print(f"File size limit reached. Stopping.")
                        sys.exit(0)  # stopping spider at 1mb domain name file size

        # Follow links to other pages
        for next_page in response.css('a::attr(href)').extract():
            yield response.follow(next_page, self.parse)

