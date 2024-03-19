from random import choice
from typing import List

import redis
from exceptions import PoolEmptyException
from loguru import logger
from schemas.proxy import Proxy
from setting import (
    PROXY_SCORE_INIT,
    PROXY_SCORE_MAX,
    PROXY_SCORE_MIN,
    REDIS_CONNECTION_STRING,
    REDIS_DB,
    REDIS_HOST,
    REDIS_KEY,
    REDIS_PASSWORD,
    REDIS_PORT,
)
from utils.proxy import convert_proxy_or_proxies, is_valid_proxy

REDIS_CLIENT_VERSION = redis.__version__
IS_REDIS_VERSION_2 = REDIS_CLIENT_VERSION.startswith('2.')


class RedisClient(object):
    """
    redis connection client of proxypool
    """

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB,
                 connection_string=REDIS_CONNECTION_STRING, **kwargs):
        """
        初始化Redis客户端，即连接Redis服务端
        :param host: redis host
        :param port: redis port
        :param password: redis password
        :param connection_string: redis connection_string
        """
        # if set connection_string, just use it
        if connection_string:
            self.db = redis.StrictRedis.from_url(connection_string, decode_responses=True, **kwargs)
        else:
            self.db = redis.StrictRedis(
                host=host, port=port, password=password, db=db, decode_responses=True, **kwargs)

    def add(self, proxy: Proxy, score=PROXY_SCORE_INIT):
        """
        添加代理并设置分数
        :param proxy: proxy, ip:port, like 8.8.8.8:88
        :param score: int score
        :return: result
        """
        if not is_valid_proxy(f'{proxy.host}:{proxy.port}'):
            logger.info(f'invalid proxy {proxy}, throw it')
            return
        if not self.exists(proxy):
            if IS_REDIS_VERSION_2:
                return self.db.zadd(REDIS_KEY, score, proxy.string())
            return self.db.zadd(REDIS_KEY, {proxy.string(): score})

    def random(self) -> Proxy:
        """
        获取随机代理
        firstly try to get proxy with max score
        if not exists, try to get proxy by rank
        if not exists, raise error
        :return: proxy, like 8.8.8.8:8
        """
        # 优先使用最大分数的代理
        proxies = self.db.zrangebyscore(
            REDIS_KEY, PROXY_SCORE_MAX, PROXY_SCORE_MAX)
        if len(proxies):
            return convert_proxy_or_proxies(choice(proxies))
        # 之后按照分数排名获取代理
        proxies = self.db.zrevrange(
            REDIS_KEY, PROXY_SCORE_MIN, PROXY_SCORE_MAX)
        if len(proxies):
            return convert_proxy_or_proxies(choice(proxies))
        # else raise error
        raise PoolEmptyException

    def decrease(self, proxy: Proxy):
        """
        代理检测为无效时，将其分数减1，当分数小于最小值则删除
        :param proxy: proxy
        :return: new score
        """
        if IS_REDIS_VERSION_2:
            self.db.zincrby(REDIS_KEY, proxy.string(), -1)
        else:
            self.db.zincrby(REDIS_KEY, -1, proxy.string())
        score = self.db.zscore(REDIS_KEY, proxy.string())
        logger.info(f'{proxy.string()} score decrease 1, current {score}')
        if score <= PROXY_SCORE_MIN:
            logger.info(f'{proxy.string()} current score {score}, remove')
            self.db.zrem(REDIS_KEY, proxy.string())

    def exists(self, proxy: Proxy) -> bool:
        """
        代理是否存在，存在返回True
        :param proxy: proxy
        :return: if exists, bool
        """
        return not self.db.zscore(REDIS_KEY, proxy.string()) is None

    def max(self, proxy: Proxy) -> int:
        """
        将代理设置为最大分数
        :param proxy: proxy
        :return: new score
        """
        logger.info(f'{proxy.string()} is valid, set to {PROXY_SCORE_MAX}')
        if IS_REDIS_VERSION_2:
            return self.db.zadd(REDIS_KEY, PROXY_SCORE_MAX, proxy.string())
        return self.db.zadd(REDIS_KEY, {proxy.string(): PROXY_SCORE_MAX})

    def count(self) -> int:
        """
        返回当前集合中元素的个数
        :return: count, int
        """
        return self.db.zcard(REDIS_KEY)

    def all(self) -> List[Proxy]:
        """
        返回所有代理组成的列表
        :return: list of proxies
        """
        return convert_proxy_or_proxies(self.db.zrangebyscore(REDIS_KEY, PROXY_SCORE_MIN, PROXY_SCORE_MAX))

    def batch(self, cursor, count):
        """
        get batch of proxies
        :param cursor: scan cursor
        :param count: scan count
        :return: list of proxies
        """
        cursor, proxies = self.db.zscan(REDIS_KEY, cursor, count=count)
        return cursor, convert_proxy_or_proxies([i[0] for i in proxies])


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.random()
    print(result)
