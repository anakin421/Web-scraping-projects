# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from sqlite3 import Error
from scrapy.exceptions import DropItem


class databaseConnection():

    """
    this class is used for various sqlite3 database operations.. 
    """

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        try:
            self.conn = sqlite3.connect("/home/abhishek/abhishek/scrapping/stack_overflow/stack_overflow/stack_overflow_db.db")
        except Error as e:
            print(f"unsuccessful!! Error is: {e}")

        self.cur = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    def execute_query(self,query):

        # self.cur.execute("PRAGMA foreign_keys = ON")

        try:
            if type(query)==tuple:
                self.cur.execute(*query)
            else: 
                self.cur.execute(query)

            data = self.cur.fetchall()
            return data
        except Error as e:
            print(f"unsuccessful!! Error is: {e}")
        finally:
            self.conn.commit()


class StackOverflowPipeline(object):

    def __init__(self):
        self.db_obj = databaseConnection()


    def store_db(self,item):

        query = f"select id from user where so_user_id = ?", (item["user_id"],)
        x = self.db_obj.execute_query(query)

        if len(x) == 0:

            query = f"INSERT INTO user (so_user_id,name,rep_score,bronze,silver,gold) values(?,?,?,?,?,?)", (item["user_id"],item["user_name"],item['user_rep'],item['bronze'],item['silver'],item['gold'])
            self.db_obj.execute_query(query)

            query = f"select id from user where so_user_id = ?", (item["user_id"],)
            u_id = self.db_obj.execute_query(query)

            fk_user_id = u_id[0][0]
        else:
            fk_user_id = x[0][0]

        """ question store here """

        query = f"INSERT INTO question (id,title,view_count,vote,total_ans,description,que_time,user_id,keyword1,keyword2,keyword3,keyword4,keyword5) values(?,?,?,?,?,?,?,?,?,?,?,?,?)", (item["que_id"],item["que_title"],item["view_count"],item['vote_count'],item["answer_count"],item['que_summary'],item["que_time"],fk_user_id,item['keyword1'],item['keyword2'],item['keyword3'],item['keyword4'],item['keyword5'])
        self.db_obj.execute_query(query)

        """ question comment store here """

        ques_comm_dict = item['ques_comm_dict']

        for i in ques_comm_dict:

            query = f"INSERT INTO question_comment (que_id,username,comment,comm_time) values (?,?,?,?)", (item["que_id"],ques_comm_dict[i]["comm_user"],ques_comm_dict[i]["comm_summary"],ques_comm_dict[i]["comm_time"])
            self.db_obj.execute_query(query)

        """ answer store here """

        answer_dict = item['answer_dict']

        for i in answer_dict:

            query = f"select id from user where so_user_id = ?", (answer_dict[i]["ans_user_id"],)
            y = self.db_obj.execute_query(query)

            if len(y) == 0:

                query = f"INSERT INTO user (so_user_id,name,rep_score,bronze,silver,gold) values(?,?,?,?,?,?)", (answer_dict[i]["ans_user_id"],answer_dict[i]["ans_user_name"],answer_dict[i]["ans_user_rep"],answer_dict[i]["ans_bronze"],answer_dict[i]["ans_silver"],answer_dict[i]["ans_gold"])
                self.db_obj.execute_query(query)

                query = f"select id from user where so_user_id = ?", (answer_dict[i]["ans_user_id"],)
                ans_u_id = self.db_obj.execute_query(query)

                fk_ans_user_id = ans_u_id[0][0]
            else:
                fk_ans_user_id = y[0][0]

            query = f"INSERT INTO answer (que_id,user_id,vote,acceptance,description,ans_time) values (?,?,?,?,?,?) ", (item["que_id"],fk_ans_user_id,answer_dict[i]["ans_vote_count"],answer_dict[i]["ans_res_accept"],answer_dict[i]["ans_info"],answer_dict[i]["ans_time"])
            self.db_obj.execute_query(query)

            query = f"select id from answer ORDER BY id DESC LIMIT 1"
            a_id = self.db_obj.execute_query(query)
            ans_id = a_id[0][0]

            """ answer comment store here """

            for j in answer_dict[i]['answer_comment']:
            
                query = f"INSERT INTO answer_comment (ans_id,username,comment,comm_time) values (?,?,?,?)", (ans_id,answer_dict[i]['answer_comment'][j]['ans_comm_user'],answer_dict[i]['answer_comment'][j]['ans_comm_summary'],answer_dict[i]['answer_comment'][j]['ans_comm_time'])
                self.db_obj.execute_query(query)


    def check_duplication(self,item): 

        """
        this method is for checking if the question is already stored in the database or not. if the question is already stored in the 
        database then it call the DropItem exception and drop that item.
        """

        query = "select id from question where id = ?", (item["que_id"],)
        x = self.db_obj.execute_query(query)

        if len(x):
            raise DropItem(item)
        else:
            return True

    def process_item(self, item, spider):

        if (self.check_duplication(item)):
            self.store_db(item)

        return item
