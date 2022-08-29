import scrapy
from itemloaders.processors import TakeFirst


class GulahmadItem(scrapy.Item):

        product_details = scrapy.Field(output_processor=TakeFirst())
        features = scrapy.Field(output_processor=TakeFirst())
        product_title = scrapy.Field(output_processor=TakeFirst())
        sale_price = scrapy.Field(output_processor=TakeFirst())
        old_price = scrapy.Field(output_processor=TakeFirst())
        sku = scrapy.Field(output_processor=TakeFirst())
        description = scrapy.Field()
        category = scrapy.Field(output_processor=TakeFirst())
        product_url = scrapy.Field(output_processor=TakeFirst())
