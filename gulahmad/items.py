import scrapy
from itemloaders import Identity


class GulahmadItem(scrapy.Item):

        product_details = scrapy.Field()
        features = scrapy.Field()
        product_title = scrapy.Field()
        sale_price = scrapy.Field()
        old_price = scrapy.Field()
        sku = scrapy.Field()
        description = scrapy.Field()
        category = scrapy.Field()
        product_url = scrapy.Field()
