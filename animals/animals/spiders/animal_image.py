import hashlib
from urllib.parse import urljoin

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AnimalImageSpider(CrawlSpider):
    """
    Этот паук обходит веб-сайт (unsplash.com), чтобы извлечь изображения животных.
    Он начинает с URL "https://unsplash.com/images/animals" и следует за ссылками на изображения
    внутри категорий.

    Атрибуты:
    - name: Название паука
    - allowed_domains: Домен(ы), которые паук имеет право обходить
    - start_urls: Начальный(ые) URL для начала обхода
    - rules: Правила для обхода, здесь следует за ссылками в определенном XPath

    Методы:
    - parse_category: Извлекает ссылки на изображения внутри категории
    - parse_image: Извлекает детали изображения, такие как автор, описание, дата публикации и
    URL изображения.

    Используется LinkExtractor для ограничения обхода по определенному XPath и возвращает результаты
    деталей изображения в формате словаря.
    """
    name = "animal_image"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/images/animals"]

    rules = (Rule(LinkExtractor(restrict_xpaths="//a[@class='Dl7bE']"),
                  callback="parse_category", follow=True),)

    def parse_category(self, response):
        post_links = response.css(".rEAWd")
        category = response.xpath("//div[@class='Aa1sS sjMaL']/h1/text()").get().split()[0].lower()
        for post_link in post_links:
            link = post_link.css("::attr(href)").get()
            post_url = urljoin('https://unsplash.com/', link)
            yield response.follow(
                post_url,
                self.parse_image,
                meta={'category': category}
            )

    @staticmethod
    def parse_image(response):
        category = response.request.meta['category']
        author_image = response.xpath("//div[@class='TO_TN']/a/text()").get()
        description = response.xpath("//h1[@class='la4U2']/text()").get()
        published = response.xpath("//time/text()").get()

        image_url = response.xpath("//div[@class='MorZF']/img/@src").get()
        article = hashlib.sha1(response.url.encode()).hexdigest()

        yield {
            'article': article,
            'category': category,
            'author_image': author_image,
            'description': description,
            'published': published,
            'image_urls': [image_url]
        }
