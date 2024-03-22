# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import logging

import aiohttp

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter, is_item
from scrapy import signals


class ProxyMiddleware:
    proxypool_url = 'http://localhost:5555/random'
    logger = logging.getLogger('middlewares.proxy')

    async def process_request(self, request, spider):
        async with aiohttp.ClientSession() as client:
            response = await client.get(self.proxypool_url)
            if not response.status == 200:
                return
            proxy = await response.text()
            self.logger.debug(f'set proxy {proxy}')
            request.meta['proxy'] = f'http://{proxy}'
