# -*- coding: utf-8 -*-
import scrapy
import re
import csv
from scrapyToJianshu.items import TaobaoItem


class TaobaoSpider(scrapy.Spider):
    name = 'TbCpuI38100'
    start_url = 'https://s.taobao.com/search?q=cpu+I3+8100&ie=utf-8'
    detail_urls = []
    data = []

    def start_requests(self):
        for i in range(1):  # 爬31页数据差不多了
            url = self.start_url + '&s=' + str(i * 44 + 1)
            yield scrapy.FormRequest(url=url, callback=self.parse)

    def url_decode(self, temp):
        while '\\' in temp:
            index = temp.find('\\')
            st = temp[index:index + 7]
            temp = temp.replace(st, '')

        index = temp.find('id')
        temp = temp[:index + 2] + '=' + temp[index + 2:]
        index = temp.find('ns')
        temp = temp[:index] + '&' + 'ns=' + temp[index + 2:]
        index = temp.find('abbucket')
        temp = 'https:' + temp[:index] + '&' + 'abbucket=' + temp[index + 8:]
        return temp

    def str_unicode(self, temp):
        while '\\' in temp:
            index = temp.find('\\')
            st = temp[index:index + 7]
            temp = temp.replace(st, '\\')

        return temp

    def parse(self, response):
        item = response.xpath('//script/text()').extract()
        pat = '"raw_title":"(.*?)","pic_url":"(.*?)","detail_url":"(.*?)","view_price":"(.*?)","item_loc":"(.*?)","view_sales":"(.*?)","comment_count":"(.*?)","nick":"(.*?)"'
        urls = re.findall(pat, str(item))
        for url in urls:  # 解析url并放入数组中
            weburl = self.url_decode(temp=url[2])
            item = TaobaoItem()
            item['title'] = self.str_unicode(temp=url[0])
            item['goods_url'] = weburl
            item['price'] = url[3]
            item['location'] = url[4]
            item['count'] = url[5]
            item['shopname'] = url[7]
            # row['price'] = item['price']
            # row['link'] = item['link']
            # self.db.insert(row)
            # row = {}.fromkeys(['name', 'price', 'link'])
            # self.detail_urls.append(weburl)
            # self.data.append(item)
            yield item

        # for item in self.detail_urls:  # 这个可以抓取评论等更多相关信息
        #     yield scrapy.FormRequest(url=item, callback=self.detail)

    # def detail(self, response):
    #     print(response.url)
    #     # 首先判断url来自天猫还是淘宝
    #     if 'tmall' in str(response.url):
    #         pass
    #     else:
    #         pass