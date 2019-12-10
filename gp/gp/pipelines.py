# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#from gp.connections import *
#from gp.items import GpItem
#from gp.models import *

import codecs
import csv


class GpPipeline(object):  # to deal with the item, put in csv.

    def __init__(self):
        self.file = codecs.open('gp.csv', 'w', encoding='utf_8_sig')

    def process_item(self, item, spider):
        fieldnames = ['gp_name','gp_downloads', 'gp_reviews','gp_tag','gp_rating','gp_package','gp_developer','gp_url','gp_intro','gp_version','gp_update','gp_news','gp_picture','gp_video_image','gp_video_url','updated_at']
        w = csv.DictWriter(self.file, fieldnames=fieldnames)
        w.writerow(item)
        return item

    def close_spider(self, spider):
        self.file.close()

'''
    def __init__(self):
        self.session = db_session()


    def process_item(self, item, spider):
        print('process item from gp url = ', item['gp_url'])

        if isinstance(item, GpItem):

            session = self.session()

            model = Product()
            model.updated_at = item['updated_at']
            model.gp_icon = item['gp_icon']
            model.gp_name = item['gp_name']
            model.gp_tag = item['gp_tag']
            model.gp_url = item['gp_url']
            model.gp_intro = item['gp_intro']
            model.gp_developer = item['gp_developer']
            model.gp_rating = item['gp_rating']
            model.gp_package = item['gp_package']
            model.gp_version = item['gp_version']
            model.gp_update = item['gp_update']
            model.gp_news = item['gp_news']
            model.gp_video_image = item['gp_video_image']
            model.gp_video_url = item['gp_video_url']
            model.gp_downloads = item['gp_downloads']
            model.gp_picture = item['gp_picture']

            try:
                m = session.query(Product).filter(Product.gp_url == model.gp_url).first()

                if m is None:  # 插入数据
                    print('add model from gp url ', model.gp_url)
                    session.add(model)
                    session.flush()
                    product_id = model.id
                else:  # 更新数据
                    print("update model from gp url ", model.gp_url)
                    m.updated_at = item['updated_at']
                    m.gp_icon = item['gp_icon']
                    m.gp_name = item['gp_name']
                    m.gp_tag = item['gp_tag']
                    m.gp_url = item['gp_url']
                    m.gp_intro = item['gp_intro']
                    m.gp_developer = item['gp_developer']
                    m.gp_rating = item['gp_rating']
                    m.gp_package = item['gp_package']
                    m.gp_version = item['gp_version']
                    m.gp_update = item['gp_update']
                    m.gp_news = item['gp_news']
                    m.gp_video_image = item['gp_video_image']
                    m.gp_video_url = item['gp_video_url']
                    m.gp_downloads = item['gp_downloads']
                    m.gp_picture = item['gp_picture']

                    product_id = m.id

                session.commit()
                print('spider_success')
            except Exception as error:
                session.rollback()
                print('gp error = ', error)
                print('spider_failure_exception')
                raise
            finally:
                session.close()
        return item

'''