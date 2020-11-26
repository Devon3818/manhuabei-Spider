# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class TutorialItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    one_field = Field()
    another_field = Field()

class CartoonItem(Item):
    id = Field()
    name = Field()
    des = Field()
    cover = Field()
    author = Field()
    status = Field()
    typeTag = Field()
    classTag = Field()
    area = Field()
    alias = Field()
    updateTime = Field()
    chapter = Field()

class SectionItem(Item):
    title = Field()
    name = Field()
    href = Field()
    index = Field()
    picture = Field()

