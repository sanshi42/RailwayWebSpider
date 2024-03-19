import scrapy


class WanfangdataSpider(scrapy.Spider):
    name = "wanfangdata"
    allowed_domains = ["s.wanfangdata.com.cn"]
    start_urls = ["https://s.wanfangdata.com.cn/advanced-search/paper"]

    def parse(self, response):
        pass
