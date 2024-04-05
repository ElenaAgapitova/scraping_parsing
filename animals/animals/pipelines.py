import scrapy

from scrapy.pipelines.images import ImagesPipeline


class AnimalsImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item.get('image_urls', []):
            yield scrapy.Request(image_url)

    def file_path(self, request, response=None, info=None, *, item=None):
        return f"{item['category']}_{item['article']}.jpg"
