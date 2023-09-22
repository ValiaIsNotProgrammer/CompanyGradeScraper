from scrapy.selector import SelectorList
from scrapy_splash import SplashRequest, SplashResponse

from .base_spider import AbstractSpider, RedirectSpider
from items import CompanyItem


class NoprizSpider(AbstractSpider, RedirectSpider):
    name = "nopriz"
    url = "https://reestr.nopriz.ru/sro/list"
    lua_div_index = 0
    current_page = 1
    custom_settings = {
        'ITEM_PIPELINES': {
            'pipelines.NoprizPipeline': 300,
        },
    }

    def start_requests(self):
        yield SplashRequest(self.url, self.parse, args={'render_all': 1, 'wait': 5})

    async def parse(self, response: SplashResponse, **kwargs):
        number_pages = self.get_number_pages(response)
        for index, div in enumerate(response.css('div.card'), start=1):
            self.lua_div_index = index
            company_item = await self._parse_to_values(div)

            yield company_item

        self.current_page += 1
        print(self.current_page)

        if self.current_page < number_pages:
            params = {"button_path": f'button[aria-label="Goto Page {self.current_page}"]', "fast_load": "true"}
            response = await self.render_from_button(params)
            yield response.follow(response.url)
        else:
            print("Reached the last page")

    async def _parse_to_values(self, tag: SelectorList) -> CompanyItem:
        item = CompanyItem()
        item["status"] = tag.xpath('.//div[@class="card__header"]//div[1]').xpath('@title').get()
        item["name"] = tag.xpath('.//div[@class="card__header"]//div[2]').xpath('string()').get()
        item["country"] = "Российская Федерация"
        item["city"] = tag.xpath('//div[text()=" Город: "]/following-sibling::div[1]/text()').get()
        item["email"] = await self.__get_email(tag)
        print(item)
        return item

    def get_number_pages(self, response: SplashResponse) -> int:
        if not hasattr(self, 'number_pages'):
            self.number_pages = self.__count_pages(response)
        return self.number_pages

    @staticmethod
    def __count_pages(response: SplashResponse, **kwargs) -> int:
        next_page_li_element_xpath = '//button[@aria-label="Next page"]'
        max_number_page_li_element_xpath = f'{next_page_li_element_xpath}/ancestor::li[1]/preceding-sibling::li[1]'
        max_number_page_li_element_text = response.xpath(max_number_page_li_element_xpath + "/button/text()").get()
        return int(max_number_page_li_element_text)

    async def __get_email(self, tag: SelectorList) -> str:
        button = tag.xpath('.//button')
        button = button.attrib.get('class')
        params = {"button_path": f'button[class="{button}"]', "div_index": self.lua_div_index}
        response = await self.render_from_button(params)
        if self.is_gateway_timeout(response):
            return "None"
        email = response.xpath('//div[text()="Адрес электронной почты:"]/following-sibling::div[1]/text()').get()
        return email



