from itemloaders.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule

from ..items import UnsplashAnimalsItem


class AnimalsImgSpider(CrawlSpider):
    name = "animals_img"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/images/animals/cat"]

    rules = (Rule(LinkExtractor(restrict_xpaths="//a[@class='rEAWd']"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        loader = ItemLoader(item=UnsplashAnimalsItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)

        loader.add_xpath("author_image", "//div[@class='TO_TN']/a/text()")
        loader.add_xpath("description", "//h1[@class='la4U2']/text()")
        loader.add_xpath("published", "//time/text()")

        image_url = response.xpath("//div[@class='MorZF']/img/@src").get()
        loader.add_value('image_urls', image_url)

        yield loader.load_item()
