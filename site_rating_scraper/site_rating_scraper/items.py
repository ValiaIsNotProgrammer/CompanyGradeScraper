import scrapy


class CompanyItem(scrapy.Item):
    name = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    status = scrapy.Field()
    email = scrapy.Field(default="None")
