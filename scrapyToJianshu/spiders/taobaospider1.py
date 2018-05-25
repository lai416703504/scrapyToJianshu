# -*- coding: utf-8 -*-
import scrapy
from scrapyToJianshu.items import TaobaoItem
from  abc import abstractmethod
import re

class TaobaoSpider(scrapy.Spider):
    base_url = "s.taobao.com"
    # name = 'jianshuspider'
    allowed_domains = [base_url]
    # start_urls = ['http://www.jianshu.com/']
    category_code = ''
    common_url = ''
    url = ''

    @abstractmethod
    def parse_more(self):
        pass

    def get_full_url(self, url):
        return self.base_url + url

    def parse(self, response):
        for i in response.xpath("//div[@id='mainsrp-itemlist']/div/div/div/div"):
            item = TaobaoItem()
            try:
                item['pic_url'] = i.xpath("./div[1]/div//div[@class='pic']/a/img/@src").extract()[0]
            except Exception as e:
                item['pic_url'] = ''

            try:
                item['price'] = i.xpath("./div[2]/div[1]/div[contains(@class,'price')]/strong/text()").extract()[0]
            except Exception as e:
                item['price'] = '0.00'

            try:
                item['count'] = re.sub('人付款','',i.xpath("./div[2]/div[1]/div[@class='deal-cnt']/text()").extract()[0])
            except Exception as e:
                item['count'] = ''

            try:
                item['title'] = re.sub('\s+','',i.xpath("./div[2]/div[2]/a/text()").extract()[0])
            except Exception as e:
                item['title'] = ''

            try:
                item['goods_url'] = i.xpath("./div[2]/div[2]/a/@href").extract()[0]
            except Exception as e:
                item['goods_url'] = ''

            try:
                item['location'] = i.xpath("./div[2]/div[3]/div[@class='location']/text()").extract()[0]
            except Exception as e:
                item['location'] = ''

            try:
                item['shopname'] = i.xpath("./div[2]/div[3]/div[@class='shop']/a/span[last()]/text()").extract()[0]
            except Exception as e:
                item['shopname'] = ''

            try:
                item['shop_url'] = i.xpath("./div[2]/div[3]/div[@class='shop']/a/@href").extract()[0]
            except Exception as e:
                item['shop_url'] = ''



        yield self.parse_more()


'''cpu I3 8100 专题'''
class TbCpuI38100Spider(TaobaoSpider):
    name = 'TbCpuI381000000'
    s = 1
    category_code = 'search'
    common_url = 'https://s.taobao.com/' + category_code + '?q=cpu+I3+8100&ie=utf-8&s='
    url = common_url + str(s)
    start_urls = [url]

    def parse_more(self):
        self.s += 44

        #每天抓20页
        if self.s > 44:
            return
        return scrapy.Request(self.common_url + str(self.s),callback=self.parse)