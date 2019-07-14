# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item


class XiguageDemoItem(Item):
    url = Field()
    title = Field()
    actor = Field()
    author = Field()
    category = Field()
    area = Field()
    time = Field()
    introduction = Field()
