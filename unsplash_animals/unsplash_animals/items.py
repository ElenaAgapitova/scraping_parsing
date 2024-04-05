# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UnsplashAnimalsItem(scrapy.Item):
    author_image = scrapy.Field()
    description = scrapy.Field()
    published = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
