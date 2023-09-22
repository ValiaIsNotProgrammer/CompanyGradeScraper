from scrapy.selector import SelectorList
from scrapy_splash import SplashRequest, SplashResponse

from .base_spider import AbstractSpider, RedirectSpider
# from settings import PROXY_LIST



class EgrzSpider(AbstractSpider, RedirectSpider):
    name = "egrz"
    url = "https://egrz.ru/organisation/reestr/latest"
    lua_div_index = 0
    current_page = 1
    custom_settings = {
        'ITEM_PIPELINES': {
            'pipelines.EgrzPipeline': 300,
        },
    }

    def start_requests(self):
        scroll_buttons_path = 'select[title="150"]'
        print(scroll_buttons_path)
        splash_args = {
            'lua_source': self.__get_lua_script(),
            "scroll_buttons_path": scroll_buttons_path,
            'render_all': 1,
            'wait': 5,
            # "fast_load": "true"
        }
        yield SplashRequest(self.url, self.parse, args=splash_args)

    async def parse(self, response: SplashResponse, **kwargs):
        print(response)
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

    async def _parse_to_values(self, tag: SelectorList) -> tuple:
        pass

    @staticmethod
    def get_number_pages(response):
        pass



    @staticmethod
    def __get_lua_script():
        with open('site_rating_scraper/spiders/utils/parse_count_result.lua', 'r') as lua_file:
            script = lua_file.read()
            return script
