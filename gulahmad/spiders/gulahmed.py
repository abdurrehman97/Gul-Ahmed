import scrapy
from itemloaders.processors import Join
from gulahmad.items import GulahmadItem
from scrapy.loader import ItemLoader
import w3lib.html


class GulAhmedSpider(scrapy.Spider):
    name = 'gulahmed'
    start_urls = ['https://www.gulahmedshop.com']

    def parse(self, response, **kwargs):

        category_list = response.css('div .menu-container li a ::attr(href)').getall()
        for url in category_list:
            if 'http' not in url:
                yield scrapy.Request(
                    url=response.urljoin(url),
                    callback=self.parse_product_categories
                )

    def parse_product_categories(self, response):
        product_listing = response.css('.product-item-photo::attr(href)').getall()
        for url in product_listing:
            yield scrapy.Request(
                url,callback=self.parse_product
            )
        next_page_url = response.css('.products + .toolbar .pages-items:not(.mobile-show) .next:not(.jump)::attr(href)').get()
        if next_page_url:
            yield scrapy.Request(
                next_page_url, callback=self.parse_product_categories
            )

    def parse_product(self, response):

        loader = ItemLoader(item=GulahmadItem(), response=response)

        varieties_of_outfits = response.css('.breadcrumbs span[itemprop="name"]::text').getall()

        sku_number = response.css('div[itemprop="sku"]::text').get()
        sku_number = sku_number.replace(' ', '')

        outfit_detail = response.css('div.description div.value :not(style)::text').getall()
        outfit_detail = [p.strip() for p in outfit_detail if p.strip()]
        outfit_detail = ''.join(outfit_detail).strip(':').strip().strip('"').strip()
        outfit_detail = w3lib.html.remove_tags(outfit_detail)

        loader.add_value('sku', sku_number)
        loader.add_css('product_title', 'span.base::text')
        loader.add_value('product_details', outfit_detail)
        loader.add_value('features', self.extract_features(response))
        loader.add_css('sale_price', 'span[data-price-type=finalPrice]::attr(data-price-amount)')
        loader.add_css('old_price', 'span[data-price-type=oldPrice]::attr(data-price-amount)')
        loader.add_value('category', varieties_of_outfits[1:-1], Join(' > '))
        loader.add_value('product_url', response.url)

        yield loader.load_item()

    def extract_features(self, response):
        features = {}
        for feature_tr in response.css("#product-attribute-specs-table tr"):
            feature_name = feature_tr.css("th::text").get()
            feature_value = feature_tr.css("td::text").get()
            features[feature_name] = feature_value

        return features
