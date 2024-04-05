"""
Команды в терминале:
    scrapy startproject trading_economics - создаем проект "trading_economics" (или иное название)
    cd trading_economics - переходим в папку trading_economics

    scrapy genspider countries "https://tradingeconomics.com/country-list/inflation-rate?continent=world" -
    создаем паука с именем countries (создается файл countries.py со стартовым кодом
    класса CountriesSpider(scrapy.Spider)

    scrapy crawl countries - запуск паука

    scrapy crawl countries -o inflation.json - экспорт данных в json
"""

import scrapy


class CountriesSpider(scrapy.Spider):
    name = "countries"
    allowed_domains = ["tradingeconomics.com"]
    start_urls = ["https://tradingeconomics.com/country-list/inflation-rate?continent=world"]

    def parse(self, response):
        countries = response.xpath('//td/a')
        for country in countries:
            name_country = country.xpath('.//text()').get().strip()
            link = country.xpath('.//@href').get()
            yield response.follow(
                url=link,
                meta={'country': name_country},
                callback=self.parse_country
            )

    @staticmethod
    def parse_country(response):
        rows = response.xpath("//tr[contains(@class, 'datatable')]")

        for row in rows:
            name = response.request.meta['country']
            related = row.xpath('.//td[1]/a/text()').get().strip()
            last_value = float(row.xpath('.//td[2]/text()').get())
            previous_value = float(row.xpath('.//td[3]/text()').get())
            unit_value = row.xpath('.//td[4]/text()').get().strip()
            date_ = row.xpath('.//td[5]/text()').get().strip()

            yield {
                'date': date_,
                'country': name,
                'related': related,
                'last': last_value,
                'previous': previous_value,
                'unit': unit_value

            }
