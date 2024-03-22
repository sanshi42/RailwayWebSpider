import time
from typing import Any, Iterable

import scrapy
from items import RailwaywebspiderItem
from scrapy.http import Response
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class WanfangdataSpider(scrapy.Spider):
    name = "wanfangdata"
    allowed_domains = ["wanfangdata.com.cn"]
    start_urls = ["https://s.wanfangdata.com.cn/advanced-search/paper"]
    TIME_OUT = 10  # 最长等待时间
    cls_list = ('S969',)  # 要爬取的数据的分类号
    service = Service(executable_path=r"C:\Scoop\apps\chromedriver\122.0.6261.39\chromedriver.exe")
    option = ChromeOptions()
    # 开启无头模式所需要的设置
    # option.add_argument('--headless')  # 1. 开启无头模式，无头模式有一些元素不加载
    option.add_argument('--disable-gpu')  # 1. 开启无头模式，无头模式有一些元素不加载
    option.add_argument('window-size=1920x1080')  # 1. 开启无头模式，无头模式有一些元素不加载
    option.add_argument('--start-maximized')  # 1. 开启无头模式，无头模式有一些元素不加载
    option.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
    option.add_argument("--disable-extensions")
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)

    # def __init__(self, name: str | None = None, **kwargs: Any):
    #     super().__init__(name, **kwargs)
    #     self.browser = webdriver.Chrome(service=self.service, options=self.option)
    #     self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{
    #         'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    #         })
    #     self.wait = WebDriverWait(self.browser, self.TIME_OUT)

    def parse_detail(self, response: Response):
        """爬取详情页"""
        self.browser = webdriver.Chrome(service=self.service, options=self.option)
        self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
            })
        self.wait = WebDriverWait(self.browser, self.TIME_OUT)
        print(f'详细页爬取：{response.url}')
        self.browser.get(response.url)
        self.wait.until(EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, 'periodicalFlex')
            ))
        item = RailwaywebspiderItem()
        item['title'] = self.browser.find_element(by=By.CLASS_NAME, value='detailTitle').text
        item['summary'] = self.browser.find_element(by=By.CSS_SELECTOR, value='.summary > .text-overflow').text
        item['authors'] = self.browser.find_element(by=By.CLASS_NAME, value='detailTitle').text
        item['keywords'] = self.browser.find_element(by=By.CLASS_NAME, value='detailTitle').text
        item['organization'] = self.browser.find_element(by=By.CLASS_NAME, value='detailTitle').text
        item['periodical_name'] = self.browser.find_element(by=By.CLASS_NAME, value='detailTitle').text
        item['issn'] = self.browser.find_element(by=By.CLASS_NAME, value='detailTitle').text
        item['publish_data'] = self.browser.find_element(by=By.CLASS_NAME, value='detailTitle').text
        item['cls_num'] = self.browser.find_element(by=By.CLASS_NAME, value='detailTitle').text
        item['cls_name'] = self.browser.find_element(by=By.CLASS_NAME, value='detailTitle').text
        yield item
        # 此时加载并不全面需要点击加载全部才行
        # print(title, summary)  # 成功

    def parse(self, response: Response):
        """爬取搜索页的内容，根据给定的分类号进行搜索"""
        self.browser = webdriver.Chrome(service=self.service, options=self.option)
        self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
            })
        self.wait = WebDriverWait(self.browser, self.TIME_OUT)

        self.browser.get(self.start_urls[0])
        # self.wait.until(EC.visibility_of_all_elements_located(
        #     (By.CLASS_NAME, 'ivu-select-selected-value')
        #     ))
        time.sleep(1)
        self.browser.find_element(by=By.CLASS_NAME, value='ivu-select-selected-value').click()
        lis = self.browser.find_elements(by=By.CSS_SELECTOR, value='.ivu-select-dropdown-list li')
        time.sleep(1)  # 如果不等待的话，后面会出问题，暂时没什么好办法解决
        for i in lis:
            if i.text == "中图分类号":
                i.click()
                break
        input_ = self.browser.find_element(by=By.CSS_SELECTOR, value='input.ivu-input')
        # sub_win_url = []  # 详细页的页面url
        for cls_num in self.cls_list:
            input_.send_keys(cls_num)
            self.wait.until(EC.visibility_of_all_elements_located(
                (By.CLASS_NAME, 'submit-btn')))
            button = self.browser.find_element(by=By.CLASS_NAME, value='submit-btn')
            button.click()
            time.sleep(1)
            # self.wait.until(EC.visibility_of_all_elements_located(
            #     (By.CSS_SELECTOR, '.detail-list-wrap > div > div')))
            while True:
                data_list = self.browser.find_elements(by=By.CSS_SELECTOR, value='.detail-list-wrap > div > div')[:20]
                for data_item in data_list:
                    self.wait.until(EC.visibility_of_all_elements_located(
                        (By.CSS_SELECTOR, 'span.title')))
                    data_item.find_element(by=By.CSS_SELECTOR, value='span.title').click()
                    self.browser.switch_to.window(self.browser.window_handles[-1])  # 第一个页面是父页面，第二个是子页面
                    # sub_win_url.append(self.browser.current_url)
                    yield scrapy.Request(self.browser.current_url, callback=self.parse_detail, priority=2)
                    self.browser.close()
                    self.browser.switch_to.window(self.browser.window_handles[0])
                try:
                    next_page = self.browser.find_element(by=By.XPATH, value='//*[@class="next"]')
                    next_page.click()
                    print('换页成功！')
                except:
                    break
        # # print(len(sub_win_url), sub_win_url)
        # assert 1==0
        # # 7. 获取相关的数据（暂时省略等待的语句，后续如果需要再补充）
        # self.wait.until(EC.visibility_of_all_elements_located(
        #     (By.CLASS_NAME, 'periodicalFlex')
        #     ))
        # title = self.browser.find_element(by=By.CLASS_NAME, value='detailTitle').text
        # summary = self.browser.find_element(by=By.CSS_SELECTOR, value='.summary > .text-overflow').text
        # # 此时加载并不全面需要点击加载全部才行
        # print(title, summary)  # 成功