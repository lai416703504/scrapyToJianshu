# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapytojianshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JianShuItem(scrapy.Item):
    # id
    _id = scrapy.Field()
    # 作者昵称
    nickname = scrapy.Field()
    # 文章标题
    title = scrapy.Field()
    # 发表时间
    createTime = scrapy.Field()
    # 文章url
    content_url = scrapy.Field()
    # 文章简介
    content_summary = scrapy.Field()
    # 浏览数量
    read = scrapy.Field()
    # 评论数量
    comments = scrapy.Field()
    # 点赞数量
    like = scrapy.Field()
    # 打赏金额
    money = scrapy.Field()
    # 配图，可以为空
    content_figure_url = scrapy.Field()
    # 作者头像，可以为空
    author_icon_url = scrapy.Field()