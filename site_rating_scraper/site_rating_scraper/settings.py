
# LOG_LEVEL = 'ERROR'
# BOT_NAME = "site_rating_scraper"

SPIDER_MODULES = ["site_rating_scraper.spiders"]
NEWSPIDER_MODULE = "site_rating_scraper.spiders"

FEED_FORMAT = 'csv'
FEED_URI = 'ratings.csv'
FEED_EXPORT_FIELDS = ['name', 'city', 'country', 'status', 'email']
FEED_EXPORT_ENCODING = 'utf-8'


HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [504, 404, 200]  # Timeout response
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

SPLASH_URL = 'http://localhost:8050'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'


# USER_AGENT = {
#     'egrz': 'egrz (+https://egrz.ru/organisation/reestr/latest)',
# }

ROBOTSTXT_OBEY = False

#CONCURRENT_REQUESTS = 32

#DOWNLOAD_DELAY = 3

# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

#COOKIES_ENABLED = False

#TELNETCONSOLE_ENABLED = False

#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "ru",
#}


# SPIDER_MIDDLEWARES = {
#     # 'scrapy_splash.SplashDeduulateArgsMiddleware': 100,
#    # "site_rating_scraper.middlewares.SiteRatingScraperSpiderMiddleware": 543,
# }


# from utils.proxies import fetch_proxies
# PROXY_LIST = fetch_proxies(1000)
# PROXY_MODE = 'PROXY_NEVER'
# PROXY_MODE = 'PROXY_BYPASS'

DOWNLOADER_MIDDLEWARES = {
    # 'scrapy_proxies.RandomProxy': 100,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 130,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    "site_rating_scraper.middlewares.SiteRatingScraperDownloaderMiddleware": 543,
}

#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}


# ITEM_PIPELINES = {
#    "site_rating_scraper.pipelines.SiteRatingScraperPipeline": 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False


# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
