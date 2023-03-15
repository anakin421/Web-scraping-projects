# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StackOverflowItem(scrapy.Item):
    # define the fields for your item here like:
    que_id = scrapy.Field()
    que_title = scrapy.Field()
    vote_count = scrapy.Field()
    view_count = scrapy.Field()
    que_summary = scrapy.Field()
    que_time = scrapy.Field()
    keyword1 = scrapy.Field()
    keyword2 = scrapy.Field()
    keyword3 =  scrapy.Field()
    keyword4 =  scrapy.Field()
    keyword5 =  scrapy.Field()

    answer_count = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    user_rep = scrapy.Field()
    bronze = scrapy.Field()
    silver = scrapy.Field()
    gold = scrapy.Field()

    ques_comm_dict = scrapy.Field()
    answer_dict = scrapy.Field()