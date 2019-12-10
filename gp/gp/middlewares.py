# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

CHROME_PATH=r''
CHROME_DRIVER_PATH=r'C:\chromedriver.exe'    #the absolute path for chrome driver


from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException
import time


class ChromeDownloaderMiddleware(object):    # use selenium module to simulate the scroll down action in the search result page. 

    def __del__(self):
        self.driver.close()

    def process_request(self, request, spider):
        if request.url=='https://play.google.com/store/search?q=loan&c=apps':  # only effective for search result page. other page will further use other download middleware
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # 设置无界面
            if CHROME_PATH:
                options.binary_location = CHROME_PATH
            if CHROME_DRIVER_PATH:
                self.driver = webdriver.Chrome(chrome_options=options, executable_path=CHROME_DRIVER_PATH)  # 初始化Chrome驱动
            else:
                self.driver = webdriver.Chrome(chrome_options=options)  # 初始化Chrome驱动
            
            print('Chrome driver begin...')
            self.driver.get(request.url)  # 获取网页链接内容
            #q_num=range[1:1]
            #for i in q_num:
            i=0
            while True:
                self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')  # simulate the scroll down behavior
                time.sleep(2)
                i+=1
                if i>8:       # do 8 times to ensure all the results can be shown
                    break
                #except TimeoutException:
                #    print('超时')
                #    self.driver.execute_script('window.stop()')
                #    print('END')
                #    break
            self.driver.execute_script('window.stop()')
            print('Chrome driver end...')
            return HtmlResponse(url=request.url, body=self.driver.page_source, request=request, encoding='utf-8',
                                status=200)  # 返回HTML数据
       
        else:
            return None  # return NONE for other pages. so other pages will find the remaining middleware module to deal with


class GpSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
