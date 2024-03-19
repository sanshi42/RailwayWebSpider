# RailwayWebSpider

> 科技领域文献元数据爬取系统，以铁路领域为例。

## 一、目标

- 爬取的站点为：[万方数据](https://s.wanfangdata.com.cn/advanced-search/paper)；
- 使用JavaScript渲染而成，使用Selenium模拟浏览器进行抓取；
- 不需要登录就能爬取，但设置了一些反爬措施。限制单个IP的访问频率，超过一定的频率，便会**封禁IP**，需要使用代理；
- 需要实现以下几点功能：
  - 利用Scrapy对接Selenium实现站点的爬取逻辑。
  - 对接代理池，突破代理访问频率的限制。

### 二、步骤

## 1. 预先准备

- Scoop安装好redis并启动服务：

```bash
scoop install redis
redis-server
```

- 创建scrapy项目，并新建一个Spider：

```bash
scrapy startproject RailwayWebSpider
cd RailwayWebSpider
scrapy genspider wanfangdata s.wanfangdata.com.cn/advanced-search/paper
```

- 运行代理池：

```bash
python run.py
```

### 2. 分析

这里使用的是Ajax接口，利用JavaScript渲染而成的

### 3. 实战开始

