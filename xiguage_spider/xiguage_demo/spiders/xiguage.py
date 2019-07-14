# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from xiguage_demo.items import XiguageDemoItem


class XiguageSpider(CrawlSpider):
    name = 'xiguage'
    allowed_domains = ['xiguage.net']
    start_urls = ['https://www.xiguage.net/frim/1.html']

    rules = (
        Rule(LinkExtractor(allow=r'.+frim.+'), follow=True),
        Rule(LinkExtractor(allow=r'.+movie.+'), callback='parse_item')
    )

    def parse_item(self, response):
        detail_url = response.css('h1 a::attr(href)').extract_first()
        url = response.urljoin(detail_url)
        title = response.xpath('//dl//dd/h1/a/text()').extract_first()
        actor = response.xpath('//dl//dd//ul/li[1]/a/text()').extract()
        author = response.xpath('//dl//dd//ul/li[2]/a/text()').extract_first()
        category = response.xpath('//dl//dd//ul/li[3]/a/text()').extract_first()
        area = response.xpath('//dl//dd//ul/li[4]/a/text()').extract_first()
        year = response.xpath('//dl//dd//ul/li[5]/a/text()').extract_first()
        day = response.xpath('//dl//dd//ul/li[6]/text()').extract_first()
        time = str(year) + '.' + str(day)
        introduction = response.xpath('//dl//dd//ul/li[7]/div/text()').extract_first()
        item = XiguageDemoItem(url=url, title=title, actor=actor, author=author, category=category, area=area, time=time, introduction=introduction)
        yield item


