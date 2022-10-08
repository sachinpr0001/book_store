"""Scraper for books catalogue

Yields:
    csv: all_bookss.csv
"""
import scrapy

class BooksSpider(scrapy.Spider):
    """book scraper class

    Args:
        scrapy

    Yields:
        response
    """
    name = "books_spider"

    def start_requests(self):
        urls = ["https://books.toscrape.com/catalogue/page-1.html"]

        # Generator Function
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for value in response.css("article.product_pod"):
            image_url = value.css("img.thumbnail::attr(src)").get()
            book_title = value.css("::attr(title)").get()
            product_price = value.css("p.price_color::text").get()

            yield {
                "image_url": image_url,
                "book_title": book_title,
                "product_price": product_price,
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
