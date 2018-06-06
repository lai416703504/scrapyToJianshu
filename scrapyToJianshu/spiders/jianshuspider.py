# -*- coding: utf-8 -*-
import scrapy
from scrapyToJianshu.items import JianShuItem
from abc import abstractmethod
import re


class JianshuspiderSpider(scrapy.Spider):
    base_url = "www.jianshu.com"
    # name = 'jianshuspider'
    allowed_domains = [base_url]
    # start_urls = ['http://www.jianshu.com/']
    category_code = ''
    common_url = ''
    url = ''

    default_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.jianshu.com',
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
                item['_id'] = re.sub(pattern, '', i.xpath("./@data-note-id").extract()[0])
            except Exception as e:
                print(e)
                return
            try:
                item['nickname'] = re.sub(pattern, '', i.xpath(
                    "./div[@class='content']/div[@class='meta']/a[@class='nickname']/text()").extract()[
                    0])
            except Exception as e:
                item['nickname'] = ''
            try:
                item['title'] = re.sub(pattern, '',
                                       i.xpath("./div[@class='content']/a[@class='title']/text()").extract()[0])
            except Exception as e:
                item['title'] = ''
            try:
                content_url = 'https://www.jianshu.com' + re.sub(pattern, '',
                                                                 i.xpath(
                                                                     "./div[@class='content']/a[@class='title']/@href").extract()[
                                                                     0])
                item['content_url'] = content_url
            except Exception as e:
                item['content_url'] = ''
            try:
                item['content_summary'] = re.sub(pattern, '', i.xpath("./div[@class='content']/p/text()").extract()[0])
            except Exception as e:
                item['content_summary'] = ''
            try:
                item['content_figure_urls'] = [
                    'https:' + re.sub(pattern, '', i.xpath("./a[@class='wrap-img']/img/@src").extract()[0])]
            except Exception as e:
                item['content_figure_urls'] = ['']

            if content_url != '':
                yield scrapy.Request(
                    url=content_url,
                    method="GET",
                    callback=self.parse_content_info,
                    meta={
                        "item": item,
                    },
                    headers=self.default_headers,
                    dont_filter=False,
                )
            else:
                yield item
        # 交由之类实现具体的处理
        yield self.parse_more()

    def parse_content_info(self, response):
        '''
        解析文章内容
        :param response:
        :return:
        '''

        item = response.meta['item']
        try:
            item['create_time'] = response.xpath("//span[@class='publish-time']/text()").extract()[0]
        except Exception as e:
            item['create_time'] = ''
        try:
            item['content_wordage'] = response.xpath("//span[@class='wordage']/text()").extract()[0].replace(u'字数 ', '')
        except Exception as e:
            item['content_wordage'] = ''
        # try:
        #     item['read'] = response.xpath("//span[@class='views-count']/text()").extract()[0]
        # except Exception as e:
        #     item['read'] = ''
        # try:
        #     item['comments'] = response.xpath("//span[@class='comments-count']/text()").extract()[0]
        # except Exception as e:
        #     item['comments'] = ''
        # try:
        #     item['like'] = response.xpath("//span[@class='likes-count']/text()").extract()[0]
        # except Exception as e:
        #     item['like'] = ''
        try:
            contentList = response.xpath("//div[@class='show-content']//text()").extract()
            item['content_text'] = "".join([each for each in contentList])
        except Exception as e:
            item['content_text'] = ''

        yield item


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

        # 每天抓20页
        if self.page > 300:
            return
        return scrapy.Request(self.common_url + str(self.page), headers=self.default_headers, callback=self.parse)


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
        return scrapy.Request(self.common_url + str(self.page), headers=self.default_headers, callback=self.parse)
