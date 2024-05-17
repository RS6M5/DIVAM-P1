import scrapy
import pandas as pd

class DivanSpider(scrapy.Spider):
    name = 'divan'
    allowed_domains = ['divan.ru']
    start_urls = ['https://www.divan.ru/category/divany']

    def parse(self, response):
        products = response.css('div.catalog__item')

        for product in products:
            item = {
                'name': product.css('a.catalog__name::text').get(),
                'price': product.css('div.catalog__price-now::text').get(),
                'link': product.css('a.catalog__name::attr(href)').get()
            }
            yield item

        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def close(self, reason):
        # Called when the spider is closed, to save the data to CSV
        data = pd.DataFrame(self.crawler.stats.get_value('item_scraped_count'))
        data.to_csv('divan_products.csv', index=False)