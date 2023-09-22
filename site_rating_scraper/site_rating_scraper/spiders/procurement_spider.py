import scrapy

from .base_spider import AbstractSpider, RedirectSpider
from items import CompanyItem


class ProcurementSpider(AbstractSpider, RedirectSpider):
    name = "zakupki"
    pages_count = 100
    custom_settings = {
        'ITEM_PIPELINES': {
            'pipelines.ProcurementPipeline': 300,

        }}

    def start_requests(self):
        url = "https://zakupki.gov.ru/epz/dishonestsupplier/search/results.html?pageNumber={}"
        for i in range(self.pages_count):
            yield scrapy.Request(url=url.format(i), callback=self.parse)

    async def parse(self, response, **kwargs):
        if response.status != 200:
            yield self.retry_with_proxy(response)
        else:
            for div in response.css(".search-registry-entry-block.box-shadow-search-input"):
                company_item = await self._parse_to_values(div)
                yield company_item

    def retry_with_proxy(self, response):
        return scrapy.Request(
            response.url,
            callback=self.parse,
            meta={'use_proxy': True},
            dont_filter=True
        )

    async def _parse_to_values(self, tag) -> CompanyItem:
        item = CompanyItem()
        item["name"] = tag.xpath('.//div[@class="registry-entry__body-value"]/text()').get()
        item["city"] = await self.__get_city(tag)
        item["country"] = self.__get_country(tag)
        item["status"] = " Исключено "
        return item

    async def __get_city(self, tag):
        city_url = tag.css('a[target="_blank"]::attr(href)').extract()[-1]
        city = await self.get_value_from_redirect(city_url, '//div[@class="common-text__value"]')
        return city

    def __get_country(self, tag):
        try:
            country = tag.xpath('.//div[@class="registry-entry__body-value"]/text()')[2].get()
        except IndexError:
            country = "Российская Федерация"
        return country
