import scrapy
from itemloaders.processors import Join

from gulahmad.items import GulahmadItem
from scrapy.loader import ItemLoader


class GulAhmedSpider(scrapy.Spider):
    name = "gulahmed"
    start_urls = ['https://www.gulahmedshop.com']

    def parse(self, response, **kwargs):
        domain = 'https://www.gulahmedshop.com'
        category_list = response.css('div .menu-container li a ::attr(href)').getall()
        for url in category_list:
            if 'http' not in url:
                url = f"{domain}{url}"
            yield scrapy.Request(
                url=url,
                callback=self.parse_product_categories
            )

    def parse_product_categories(self, response):
        product_categories = response.css('.product-item-photo::attr(href)').getall()
        for url in product_categories:
            yield scrapy.Request(
                url,callback=self.parse_product_fields
            )
        pagination = response.css('.products + .toolbar .pages-items:not(.mobile-show) .next:not(.jump)::attr(href)').get()
        if pagination:
            yield scrapy.Request(
            pagination, callback=self.parse_product_categories
        )

    def parse_product_fields(self, responce):

        l = ItemLoader(item=GulahmadItem(), response=responce)

        category = responce.css('.breadcrumbs span[itemprop="name"]::text').getall()

        space = responce.css('div[itemprop="sku"]::text').get()
        sku_number = space.replace(' ', '')

        l.add_value('sku', sku_number)
        l.add_css('product_title', 'span.base::text')
        l.add_css('product_details', 'div.value p::text')
        l.add_value('features', self.extract_features(responce))
        l.add_css('sale_price', 'span[data-price-type=finalPrice]::attr(data-price-amount)')
        l.add_css('old_price', 'span[data-price-type=oldPrice]::attr(data-price-amount)')
        l.add_value('category', category[1:-1], Join(' > '))
        l.add_value('product_url', responce.url)

        yield l.load_item()

    def extract_features(self, response):
        features = {}
        for feature_tr in response.css("#product-attribute-specs-table tr"):
            feature_name = feature_tr.css("th::text").get()
            feature_value = feature_tr.css("td::text").get()
            features[feature_name] = feature_value

        return features