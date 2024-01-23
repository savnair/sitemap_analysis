import scrapy
from bs4 import BeautifulSoup

class LinkcounterSpider(scrapy.Spider):
    name = "linkcounter"

    def start_requests(self):
        # Pass the sitemap URL as a command-line argument
        sitemap_url = getattr(self, 'sitemap_url', None)
        if sitemap_url:
            yield scrapy.Request(url=sitemap_url, callback=self.parse_sitemap)

    def parse_sitemap(self, response):
        content_type = response.headers.get('Content-Type', b'').decode('utf-8').lower()
        parser = 'xml' if 'xml' in content_type else 'html.parser'
        soup = BeautifulSoup(response.text, parser)

        # Extract links using BeautifulSoup
        links = [loc.text for loc in soup.find_all('loc')]

        # Initialize a counter for links that don't lead to more links
        terminal_links_count = 0

        for link in links:
            # You can perform additional checks to identify terminal nodes
            # For simplicity, let's assume links without 'sitemap' in the URL are terminal
            if 'sitemap' not in link:
                terminal_links_count += 1
            else:
                yield response.follow(link, self.parse_sitemap)

        print(f"Number of terminal links: {terminal_links_count}")

    def parse_page(self, response):
        # Extract links using BeautifulSoup
        content_type = response.headers.get('Content-Type', b'').decode('utf-8').lower()
        parser = 'xml' if 'xml' in content_type else 'html.parser'
        soup = BeautifulSoup(response.text, parser)
        links = [a['href'] for a in soup.find_all('a', href=True)]

        # Follow links recursively
        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_page)
