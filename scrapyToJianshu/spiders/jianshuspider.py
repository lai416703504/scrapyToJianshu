# -*- coding: utf-8 -*-
import scrapy
from scrapyToJianshu.items import JianShuItem
from abc import abstractmethod
import re


class JianshuspiderSpider(scrapy.Spider):
    base_url = "www.jianshu.com"
    #name = 'jianshuspider'
    allowed_domains = [base_url]
    #start_urls = ['http://www.jianshu.com/']
    category_code = ''
    common_url = ''
    url = ''

    default_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.douban.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    @abstractmethod
    def parse_more(self):
        pass

    def get_full_url(self, url):
        return self.base_url + url


    def parse(self, response):
        for i in response.xpath("//ul[@class='note-list']/li"):
            item = JianShuItem()
            pattern = '\s+'
            try:
                item['_id'] = re.sub(pattern, '', i.xpath("./@id").extract()[0])
            except Exception as e:
                print(e)
                return
            try:
                item['nickname'] = re.sub(pattern, '', i.xpath("./div[@class='content']/div[@class='author']/div[@class='info']/a[@class='nickname']/text()").extract()[0])
            except Exception as e:
                item['nickname'] = ''
            try:
                item['title'] = re.sub(pattern, '', i.xpath("./div[@class='content']/a[@class='title']/text()").extract()[0])
            except Exception as e:
                item['title'] = ''
            try:
                item['content_url'] = re.sub(pattern, '', i.xpath("./div[@class='content']/a[@class='title']/@href").extract()[0])
            except Exception as e:
                item['content_url'] = ''
            try:
                item['content_summary'] = re.sub(pattern, '', i.xpath("./div[@class='content']/p/text()").extract()[0])
            except Exception as e:
                item['content_summary'] = ''
            try:
                item['read'] = re.sub(pattern, '', i.xpath("./div[@class='content']/div[@class='meta']/a[1]/text()[last()]").extract()[0])
            except Exception as e:
                item['read'] = '0'
            try:
                item['comments'] = re.sub(pattern, '', i.xpath("./div[@class='content']/div[@class='meta']/a[2]/text()[last()]").extract()[0])
            except Exception as e:
                item['comments'] = '0'
            try:
                item['like'] = re.sub(pattern, '', i.xpath("./div[@class='content']/div[@class='meta']/span[1]/text()[last()]").extract()[0])
            except Exception as e:
                item['like'] = '0'
            try:
                item['money'] = re.sub(pattern, '', i.xpath("./div[@class='content']/div[@class='meta']/span[2]/text()[last()]").extract()[0])
            except Exception as e:
                item['money'] = '0'
            try:
                item['content_figure_urls'] = ['http:' + re.sub(pattern, '', i.xpath("./a[@class='wrap-img']/img/@src").extract()[0])]
            except Exception as e:
                item['content_figure_urls'] = ['']
            yield item
        # 交由之类实现具体的处理
        yield self.parse_more()

'''@IT.互联网 专题'''
class ITSpider(JianshuspiderSpider):
    name = 'ITSpider'
    page = 0
    category_code = 'V2CqjW'
    common_url = 'http://www.jianshu.com/c/' + category_code + '?order_by=added_at&page='
    url = common_url + str(page)
    start_urls = [url]

    def parse_more(self):
        self.page += 1

        #每天抓20页
        if self.page > 2:
            return
        return scrapy.Request(self.common_url + str(self.page),callback=self.parse)

'''程序员 专题'''
class CoderSpider(JianshuspiderSpider):
    name = 'jianshu-coder'
    page = 0
    category_code = 'NEt52a'
    common_url = 'http://www.jianshu.com/c/' + category_code + '?order_by=added_at&page='
    url = common_url + str(page)
    start_urls = [url]

    def parse_more(self):
        self.page += 1

        if self.page > 10:
            return
        return scrapy.Request(self.common_url + str(self.page), callback=self.parse)

