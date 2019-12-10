# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GpItem(scrapy.Item):
    # define the fields for your item here like:
    updated_at = scrapy.Field()  # 最后一次更新时间
    gp_name = scrapy.Field()  # GP名称
    gp_package = scrapy.Field()  # GP包名
    gp_rating = scrapy.Field()  # GP评级
    gp_reviews = scrapy.Field()   # 评论数
    gp_downloads = scrapy.Field()  # GP下载人数 
    gp_tag = scrapy.Field()  # GP标签
    gp_url = scrapy.Field()  # GP链接
    gp_intro = scrapy.Field()  # GP介绍
    gp_developer = scrapy.Field()  # GP开发者 
  # gp_picture = scrapy.Field()  # GP图片，英文逗号分割
    gp_version = scrapy.Field()  # GP最新版本
    gp_update = scrapy.Field()  # GP更新时间
    gp_news = scrapy.Field()  # GP更新内容
    gp_video_image = scrapy.Field()  # GP视频图片
    gp_video_url = scrapy.Field()  # GP视频链接
    
