# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exporters import JsonItemExporter


class ScrapytojianshuPipeline(object):
    def process_item(self, item, spider):
        return item


'''这里网站上是想放到mongodb，我这里准备放文件里面'''


class JianshuPipeline(object):

    def __init__(self):
        # 可选实现，当spider被开启时，这个方法被调用。
        # 输出到tongcheng_pipeline.json文件
        self.file = open('jianshu.json', 'wb'
        self.exporter = JsonItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        # 可选实现，当spider被关闭时，这个方法被调用
        self.exporter.finish_exporting()
        self.file.close()
