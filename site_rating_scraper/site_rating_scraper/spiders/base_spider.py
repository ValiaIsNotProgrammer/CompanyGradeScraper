from abc import abstractmethod, ABC
from typing import Union

from scrapy import Spider
from scrapy.selector import SelectorList
from scrapy.utils.defer import deferred_to_future
from scrapy_splash import SplashResponse, SplashRequest
from scrapy.http.response import Response, Request


class RedirectSpider:

    async def get_value_from_redirect(self, url: str, element_xpath: str):
        request = self._get_request(url, {"wait": 10})
        response = await self._await_deferred(request)
        return self.parse_value(response, element_xpath)

    def parse_value(self, response, element_xpath, **kwargs):
        element = self._parse_element(response, element_xpath)
        return element

    def _get_request(self, *args, **kwargs):
        default_kwargs = {
            'url': args[0] if args else self.url,
            'callback': RedirectSpider._parse_element,
            **kwargs
        }
        request = SplashRequest(**default_kwargs)
        deferred = self.crawler.engine.download(request)
        return deferred

    async def _await_deferred(self, deferred):
        response = await deferred_to_future(deferred)
        if self.is_gateway_timeout(response):
            return response
        return response

    def _parse_element(self, response: SplashResponse, element_xpath):
        value = response.xpath(element_xpath).get()
        return value

    async def render_from_button(self, params: dict):
        with open('site_rating_scraper/spiders/utils/parse_nopriz.lua', 'r') as lua_file:
            script = lua_file.read()
        splash_args = {
            'lua_source': params["lua_source"] if params["lua_source"] else script,
            **params
        }
        request = self._get_request(endpoint="execute", args=splash_args)
        response = await self._await_deferred(request)
        return response

    @staticmethod
    def is_gateway_timeout(response):
        if response.status == 504:
            return True
        return False


class AbstractSpider(Spider, ABC):
    name = 'abstract_spider'

    @abstractmethod
    def start_requests(self) -> Union[SplashRequest, Request]:
        pass

    @abstractmethod
    def parse(self, response: Union[SplashResponse, Response], **kwargs) -> dict:
        pass

    @abstractmethod
    def _parse_to_values(self, tag: SelectorList) -> tuple:
        pass

