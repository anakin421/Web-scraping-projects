# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from .db_connect import * 


class QuotetutorialPipeline(object):

    def process_item(self, item, spider):

        self.store_db(item)
        return item

    def store_db(self,item):

        query = 'select id from quotes where title = ?', (item['title'],)
        db_obj = database(query)
        q = db_obj.execute()

        if len(q) == 0:

            query = 'select id from author where name = ?', (item['author'],)
            db_obj= database(query)
            a = db_obj.execute()

            if len(a) == 0:
                query = "insert into author (name) values (?)", (item['author'],)
                db_obj = database(query)
                db_obj.execute()

            query = 'select id from author where name = ?', (item['author'],)
            db_obj= database(query)
            author = db_obj.execute()

            taglist = item['tag']

            query = "insert into quotes (title,author_id) values (?,?)", (item['title'],author[0][0])
            db_obj = database(query)
            db_obj.execute()

            query1 = 'select max(id) from quotes'
            db_obj1 = database(query1)
            y = db_obj1.execute()  

            quote_id = y[0][0]

            for tag in taglist:
                query1 = 'select id from tag where tagname = ?', (tag,)
                db_obj1 = database(query1)
                x = db_obj1.execute()

                if len(x) == 0:
                    query = "insert into tag (tagname) values (?)", (tag,)
                    db_obj = database(query)
                    db_obj.execute()

                query = 'select id from tag where tagname = ?', (tag,)
                db_obj = database(query)
                z = db_obj.execute()

                tag_id = z[0][0]

                query = 'insert into quote_tag (quote_id,tag_id) values (?,?)', (quote_id,tag_id)
                db_obj = database(query)
                db_obj.execute()