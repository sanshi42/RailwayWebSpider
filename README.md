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

#### 3.1 定义爬取字段的Item

标题（titile）

摘要（summary）

作者（authors

作者机构organization

期刊名称（periodical_name）

ISSN（issn）

年,卷(期)（publish_data）

分类号cls_num

分类号中文名cls_name

#### 3.2 主要爬取逻辑   

- 初始的爬取请求
- 实现Spider解析的基本逻辑
  - Scrapy无法解释JavaScript代码，所以直接在解析中使用selenium
  - 完善整体逻辑，实现一个初步的爬虫
- 定义使用IP池的下载器中间件解决封IP的问题
  - 同时开启Scrapy对于协程的支持，这使用的是协程对象

- 完善Spider的逻辑
