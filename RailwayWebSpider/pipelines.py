# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from items import RailwaywebspiderItem

class MySQLPipeline:
    
    # @classmethod
    # def from_crawler(cls, crawler):
    #     cls.connection_string = crawler.settings.get()
    #     cls.database = crawler.settings.get()
    #     cls.collection = crawler.settings.get()
    #     return cls()
    
    def open_spider(self, spider):
        self.client = pymysql.connect(self.connection_string)

    def process_item(self, item, spider):
        for key, value in item.items():
            
        return item
    
    def close_spider(self, spider):
        self.client.close()
