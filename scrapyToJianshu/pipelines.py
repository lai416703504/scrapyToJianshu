# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exporters import JsonItemExporter
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
import os
import csv


class ScrapytojianshuPipeline(object):
    def process_item(self, item, spider):
        return item


'''这里网站上是想放到mongodb，我这里准备放文件里面'''


class JianshuPipeline(object):
    # def __init__(self):
    #     # 可选实现，当spider被开启时，这个方法被调用。
    #     # 输出到tongcheng_pipeline.json文件
    #     self.file = open('jianshu.json', 'wb')
    #     self.exporter = JsonItemExporter(self.file, encoding='utf-8')
    #     self.exporter.start_exporting()
    #
    # def process_item(self, item, spider):
    #     self.exporter.export_item(item)
    #     return item
    #
    # def close_spider(self, spider):
    #     # 可选实现，当spider被关闭时，这个方法被调用
    #     self.exporter.finish_exporting()
    #     self.file.close()

    '''

    上面的方法是直接生成一条JSON文件

    下面的方法适合读取文件后给Pandas 的DataFrame 生成数据

    '''
    #
    # def __init__(self):
    #     self.file = open('jianshu.txt', 'wb')
    #
    # def process_item(self, item, spider):
    #     json_item = json.dumps(dict(item))
    #     self.file.write(json_item + '\n')
    #     return item
    #
    # def close_spider(self, spider):
    #     self.file.close()

    '''写成CSV格式'''

    def __init__(self):
        # csv文件的位置，无需实现创建
        store_file = 'jianshu.csv'
        # 打开(创建)文件
        self.file = open(store_file, 'wb')
        # CSV写法
        self.writer = csv.writer(self.file)

    def process_item(self, item, spider):
        self.writer.writerow((item['_id'], item['title'].encode('utf8', 'ignore'), item['content_url'],
                           item['content_summary'].encode('utf8', 'ignore')))
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()


'''简书下载图片'''
class JianshuImagesPipeline(ImagesPipeline):
    default_headers = {
        'accept': 'image/webp,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'cookie': 'bid=yQdC/AzTaCw',
        'referer': 'https://www.douban.com/photos/photo/2370443040/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    def get_media_requests(self, item, info):
        for image_url in item['content_figure_urls']:
            self.default_headers['referer'] = image_url
            yield scrapy.Request(image_url, headers=self.default_headers)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['content_figure_paths'] = image_paths
        return item
