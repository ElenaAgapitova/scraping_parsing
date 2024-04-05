import scrapy


class AnimalsItem(scrapy.Item):
    article = scrapy.Field()
    category = scrapy.Field()
    author_image = scrapy.Field()
    description = scrapy.Field()
    published = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
