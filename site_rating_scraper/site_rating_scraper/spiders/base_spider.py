import functools
import json
from abc import abstractmethod, ABC
from typing import Union

import scrapy
from scrapy import Spider
from scrapy.selector import SelectorList
from scrapy.utils.defer import deferred_to_future
from scrapy_splash import SplashResponse, SplashRequest
from scrapy.http.response import Response, Request


class RedirectSpider:

    async def get_value_from_redirect(self: Spider, url: str, element_xpath: str):
        request = RedirectSpider._get_request(url)
        response = await RedirectSpider._await_deferred(request)
        return RedirectSpider.parse_value(response, element_xpath)

    def parse_value(self, response, element_xpath, **kwargs):
        element = RedirectSpider._parse_element(response, element_xpath)
        return element

    def _get_request(self, *args, **kwargs):
        default_kwargs = {
            'url': self.url,
            'callback': RedirectSpider._parse_element,
            **kwargs
        }
        print(kwargs['args']['button_path'])
        request = SplashRequest(**default_kwargs)
        deferred = self.crawler.engine.download(request)
        return deferred

    @staticmethod
    async def _await_deferred(deferred):
        return await deferred_to_future(deferred)

    @staticmethod
    def _parse_element(response, element_xpath):
        value = response.xpath(element_xpath).get()
        return value

    async def render_from_button(self, button_xpath):
        with open('site_rating_scraper/spiders/utils/parse_nopriz.lua', 'r') as lua_file:
            script = lua_file.read()
        splash_args = {
            'lua_source': script,
            'button_path': f'button[type="{button_xpath}"]'
        }
        request = self._get_request(endpoint="execute", args=splash_args)
        response = await self._await_deferred(request)
        print(response.text)
        return response


class AbstractSpider(Spider, RedirectSpider, ABC):
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