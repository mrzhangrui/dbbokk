# -*- coding: utf-8 -*-
import scrapy
import re
from dbbook.items import DbbookItem


class DoubanbookSpider(scrapy.Spider):
    name = "doubanbook"
    # allowed_domains = ["https://www.douban.com/doulist/1264675/"]
    start_urls = ['https://www.douban.com/doulist/1264675/']

    def parse(self, response):
        # print(response.body)
        # print(response)
        # selector = scrapy.Selector(response)
        # books = selector.xpath('//div[@class="bd doulist-subject"]')
        item = DbbookItem()
        books = response.xpath('//div[@class="bd doulist-subject"]')
        for book in books:
            title = book.xpath('div[@class="title"]/a/text()').extract()[0]
            rate = book.xpath('div[@class="rating"]/span[@class="rating_nums"]/text()').extract()[0]
            # auth=book.xpath('div[@class="abstract"/text()]').extract()[0]
            author = re.search('<div class="abstract">(.*?)<br', book.extract(), re.S).group(1)
            title = title.replace(' ', '').replace('\n', '')
            rate = rate.replace(' ', '').replace('\n', '')
            author = author.replace(' ', '').replace('\n', '')
            item['title'] = title
            item['rate'] = rate
            item['author'] = author
            yield item
            # print('标题:' + title)
            # print('评分:' + rate)
            # print(author)
            # print('\n')
        nextpage = response.xpath('//span[@class="next"]/link/@href').extract()
        if nextpage:
            next = nextpage[0]
            # print(next)
            yield scrapy.Request(next, callback=self.parse)
