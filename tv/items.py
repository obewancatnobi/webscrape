# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TvItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    Title = scrapy.Field()
    Season = scrapy.Field()
    Genre = scrapy.Field()
    Release_Date = scrapy.Field()
    Critic_Score = scrapy.Field()
    User_Score = scrapy.Field()
    Network = scrapy.Field()
    Critics_votes = scrapy.Field()
    Users_votes = scrapy.Field()
