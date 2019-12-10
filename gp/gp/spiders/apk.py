# -*- coding: utf-8 -*-
import scrapy
import re
import time
from scrapy import Request, Spider
from urllib import parse
from gp.items import GpItem



class ApkSpider(scrapy.Spider):
    name = 'apk'
    allowed_domains = ['play.google.com']
    start_urls = ['https://play.google.com/store/search?q=loan&c=apps']     # the search result page by using 'loan' as the keyword 

    def parse(self, response):

        #selector = scrapy.Selector(response)
        app_urls = response.xpath('//div[@class="wXUyZd"]/a/@href').extract()  # get all app links on the search result page
        print(app_urls)

        urls=[]

        for url in app_urls:
            url="https://play.google.com"+url
            print(url)
            urls.append(url)

        link_flag=0

        for each in urls:
            yield Request(urls[link_flag], callback=self.parse_detail, dont_filter=True)    # crawl the detail app pages
            link_flag+=1
            #if link_flag>1:
            #   break

        


    def parse_detail(self, response):    # function to crawl the detail app page
        print('Begin parse ', response.url)

        item = GpItem()

        item['updated_at'] = time.ctime()   #time.strftime("%b %d %Y",(time.time()))

        content = response.xpath('//div[@class="LXrl4c"]')

        exception_count = 0

        
        try:
            item['gp_reviews'] = response.xpath('//span[@class="AYi5wd TBRnV"]/span/text()')[0].extract()
            #print(response.xpath('//span[@class="AYi5wd TBRnv"]'))

        except Exception as error:
            #print(content.xpath('//span[@class="AYi5wd TBRnv"]'))
            exception_count += 1
            print('gp_reviews except = ', error)
            item['gp_reviews'] = ''

        try:
            item['gp_name'] = content.xpath('//h1[@class="AHFaub"]/span/text()')[0].extract()
            print(content.xpath('//h1[@class="AHFaub"]/span'))
        except Exception as error:
            exception_count += 1
            print('gp_name except = ', error)
            item['gp_name'] = ''

        try:
            item['gp_tag'] = content.xpath('//a[@itemprop="genre"]/text()')[0].extract()
        except Exception as error:
            exception_count += 1
            print('gp_tag except = ', error)
            item['gp_tag'] = ''

        item['gp_url'] = response.url

        try:
            show_more_content = content.xpath('//div[@jsname="sngebd"]/text()').extract()
            app_introduction = ''
            for more in show_more_content:
                app_introduction = app_introduction + more + '\n'
            item['gp_intro'] = app_introduction.strip('\n')
        except Exception as error:
            exception_count += 1
            print('gp_intro except = ', error)
            item['gp_intro'] = ''

        try:
            item['gp_developer'] = content.xpath('//a[@class="hrTbp R8zArc"]/text()')[0].extract()
        except Exception as error:
            exception_count += 1
            print('gp_developer except = ', error)
            item['gp_developer'] = ''

        try:
            gp_rating = content.xpath(
                '//div[@class="BHMmbe"]/text()')[
                0].extract()
            item['gp_rating'] = gp_rating.replace(',', '.')
        except Exception as error:
            exception_count += 1
            print('gp_rating except = ', error)
            item['gp_rating'] = ''

        try:
            parse_result = parse.urlparse(response.url)
            params = parse.parse_qs(parse_result.query, True)

            item['gp_package'] = params['id'][0]
        except Exception as error:
            exception_count += 1
            print('gp_package except = ', error)
            item['gp_package'] = ''


        try:
            if len(content.xpath('//div[@class="IxB2fe"]/div[1]/span/div/span[@class="htlgb"]/text()')) > 0:
                item['gp_update'] = content.xpath('//div[@class="IxB2fe"]/div[1]/span/div/span[@class="htlgb"]/text()')[0].extract().strip()
            else:
                item['gp_update'] = ''
        except Exception as error:
            exception_count += 1
            print('gp_update except = ', error)
            item['gp_update'] = ''

        try:
            recent_change = content.xpath(
                '//c-wiz[@jsrenderer="eG38Ge"]/div/div[2]/div[@class="DWPxHb"]/span/text()').extract()
            gp_news = ''
            for change in recent_change:
                gp_news = gp_news + change + '\n'
            item['gp_news'] = gp_news.strip('\n')
        except Exception as error:
            exception_count += 1
            print('gp_news except = ', error)
            item['gp_news'] = ''

        try:
            item['gp_version'] = content.xpath('//div[@class="IxB2fe"]/div[4]/span/div/span[@class="htlgb"]/text()')[0].extract().strip()
        except Exception as error:
            exception_count += 1
            print('gp_version except = ', error)
            item['gp_version'] = ''

        try:
            item['gp_downloads'] = content.xpath('//div[@class="IxB2fe"]/div[3]/span/div/span[@class="htlgb"]/text()')[0].extract().strip()
        except Exception as error:
            exception_count += 1
            print('gp_downloads except = ', error)
            item['gp_downloads'] = ''

        try:
            if len(content.xpath('//div[@class="MSLVtf NIc6yf"]/img/@src')) > 0:
                item['gp_video_image'] = response.urljoin(
                    content.xpath('//div[@class="MSLVtf NIc6yf"]/img/@src')[0].extract())
            else:
                item['gp_video_image'] = ''
        except Exception as error:
            exception_count += 1
            print('gp_video_image except = ', error)
            item['gp_video_image'] = ''

        try:
            if len(content.xpath('//button[@class="lgooh  "]/@data-trailer-url')) > 0:
                item['gp_video_url'] = content.xpath('//button[@class="lgooh  "]/@data-trailer-url')[
                    0].extract()
            else:
                item['gp_video_url'] = ''
        except Exception as error:
            exception_count += 1
            print('gp_video_url except = ', error)
            item['gp_video_url'] = ''
      
        if exception_count >= 10:
            print('spider_failure_parse_too_much_exception')
            return

        return item

