from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders.procurement_spider import ProcurementSpider
from spiders.nopriz import NoprizSpider
from spiders.egrz_spider import EgrzSpider

process = CrawlerProcess(get_project_settings())
process.crawl(EgrzSpider.name)
process.start()