# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RailwaywebspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    summary = scrapy.Field()
    authors = scrapy.Field()
    keywords = scrapy.Field()
    organization = scrapy.Field()
    periodical_name = scrapy.Field()
    issn = scrapy.Field()
    publish_data = scrapy.Field()
    cls_num = scrapy.Field()
    cls_name = scrapy.Field()
