# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field,Item


class ScrapytojianshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JianShuItem(Item):
    # id
    _id = Field()
    # 文章标题
    title = Field()
    # 作者昵称
    nickname = Field()
    # 文章url
    content_url = Field()
    # 文章简介
    content_summary = Field()
    # 文章内容
    content_text = Field()
    # 文章字数
    content_wordage = Field()
    # 浏览数量
    read = Field()
    # 评论数量
    comments = Field()
    # 点赞数量
    like = Field()
    # 配图，可以为空
    content_figure_urls = Field()
    # 发表时间
    create_time = Field()
    # 配图，下载下来
    # content_figure = Field()
    # content_figure_paths = Field()

class TaobaoItem(scrapy.Item):
    #图片地址
    # pic_url = scrapy.Field()
    #价格
    price = scrapy.Field()
    # 销量
    count = scrapy.Field()
    #标题
    title = scrapy.Field()
    # 商品链接
    goods_url = scrapy.Field()
    #店铺地址
    location = scrapy.Field()
    #店铺名
    shopname = scrapy.Field()
    #店铺链接
    # shop_url = scrapy.Field()
