import scrapy
from scrapy.utils.defer import deferred_to_future

from .base_spider import AbstractSpider


class ProcurementSpider(AbstractSpider):
    name = "zakupki"
    pages_count = 100

    def start_requests(self):
        url = "https://zakupki.gov.ru/epz/dishonestsupplier/search/results.html?pageNumber={}"
        for i in range(self.pages_count):
            yield scrapy.Request(url=url.format(i), callback=self.parse)

    async def parse(self, response, **kwargs):
        for div in response.css(".search-registry-entry-block.box-shadow-search-input"):
            number, initials, tin, country, city = await self._parse_to_values(div)
            yield {
                "number": number,
                "initials": initials,
                "tin": tin,
                "country": country,
                "city": city
            }

    async def _parse_to_values(self, tag):
        number = tag.xpath('.//div[@class="registry-entry__header-mid__number"]/a/text()').get()
        initials = tag.xpath('.//div[@class="registry-entry__body-value"]/text()').get()
        tin = tag.xpath('.//div[@class="registry-entry__body-value"]/text()')[1].get()
        city_url = tag.css('a[target="_blank"]::attr(href)').extract()[-1]
        city = await self.get_city(city_url)
        try:
            country = tag.xpath('.//div[@class="registry-entry__body-value"]/text()')[2].get()
        except IndexError:
            country = "Российская Федерация"

        return number, initials, tin, country, city












    # async def get_city(self, url):
    #     request = self.__get_city_request(url)
    #     deferred = self.crawler.engine.download(request)
    #     response = await deferred_to_future(deferred)
    #     city = self.__parse_city(response)
    #     return city
    #
    # def __get_city_request(self, url):
    #     request = scrapy.Request(url=url, callback=self.__parse_city)
    #     return request

    # @staticmethod
    # def __parse_city(response):
    #     city = response.xpath('//div[@class="common-text__value"]/text()').get()
    #     return city

