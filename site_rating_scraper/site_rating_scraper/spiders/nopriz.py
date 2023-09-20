import scrapy
import scrapy_splash
from scrapy.selector import SelectorList
from scrapy_splash import SplashRequest, SplashResponse

from .base_spider import AbstractSpider


class NoprizSpider(AbstractSpider):
    name = "nopriz"
    url = "https://reestr.nopriz.ru/sro/list"

    def start_requests(self):
        yield SplashRequest(self.url, self.parse, args={'render_all': 1, 'wait': 5})

    async def parse(self, response: SplashResponse, **kwargs):
        number_pages = self.count_pages(response)
        print(number_pages)

        for div in response.css('div.card'):
            # name, status, country, city, email = self._parse_to_values(div)
            await self._parse_to_values(div)

    async def _parse_to_values(self, tag: SelectorList) -> tuple:
        first_div = tag.xpath('.//div[@class="card__header"]//div[1]')
        second_div = tag.xpath('.//div[@class="card__header"]//div[2]')
        status = first_div.xpath('@title').get()
        name = second_div.xpath('string()').get()
        country = "Российская Федерация"
        city = tag.xpath('//div[text()=" Город: "]/following-sibling::div[1]/text()').get()

        # button_xpath = tag.xpath('.//button').attrib.get('class')
        button = tag.xpath('.//button')
        button = button.attrib['class']

        company_page = await self.render_from_button(button)
        email = company_page.xpath('//div[text()="Адрес электронной почты:"]/following-sibling::div[1]/text()').get()
        print(email)

    def count_pages(self, response: SplashResponse, **kwargs) -> int:
        next_page_li_element_xpath = '//button[@aria-label="Next page"]'
        max_number_page_li_element_xpath = f'{next_page_li_element_xpath}/ancestor::li[1]/preceding-sibling::li[1]'
        max_number_page_li_element_text = response.xpath(max_number_page_li_element_xpath + "/button/text()").get()
        return int(max_number_page_li_element_text)
