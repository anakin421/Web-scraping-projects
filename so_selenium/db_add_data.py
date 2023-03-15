from db_connect import * 

class add_data():

    def __init__(self,data):
        self.data = data

    def check_duplication(self): 

        """
        this method is for checking if the question is already stored in the database or not. if the question is already stored in the 
        database then it call the DropItem exception and drop that data.
        """

        query = "select id from question where id = ?", (self.data["que_id"],)
        db_obj = database(query)
        x = db_obj.execute()   

        if not len(x):
            self.insert_data()

    def insert_data(self):

        query = f"select id from user where so_user_id = ?", (self.data["user_id"],)
        db_obj = database(query)
        x = db_obj.execute()

        if len(x) == 0:

            query = f"INSERT INTO user (so_user_id,name,rep_score,bronze,silver,gold) values(?,?,?,?,?,?)", (self.data["user_id"],self.data["user_name"],self.data['user_rep'],self.data['user_bronze'],self.data['user_silver'],self.data['user_gold'])
            db_obj = database(query)
            db_obj.execute()

            query = f"select id from user where so_user_id = ?", (self.data["user_id"],)
            db_obj = database(query)
            fk_user_id = db_obj.execute()[0][0]
        else:
            fk_user_id = x[0][0]

        """ question store here """

        query = f"INSERT INTO question (id,title,view_count,vote,total_ans,description,que_time,user_id,keyword1,keyword2,keyword3,keyword4,keyword5) values(?,?,?,?,?,?,?,?,?,?,?,?,?)", (self.data["que_id"],self.data["que_title"],self.data["view_count"],self.data['vote_count'],self.data["answer_count"],self.data['que_summary'],self.data["que_time"],fk_user_id,self.data['keyword1'],self.data['keyword2'],self.data['keyword3'],self.data['keyword4'],self.data['keyword5'])
        db_obj = database(query)
        db_obj.execute()

        """ question comment store here """

        ques_comm_dict = self.data['ques_comm_dict']

        for i in ques_comm_dict:

            query = f"INSERT INTO question_comment (que_id,username,comment,comm_time) values (?,?,?,?)", (self.data["que_id"],ques_comm_dict[i]["comm_user"],ques_comm_dict[i]["comm_summary"],ques_comm_dict[i]["comm_time"])
            db_obj = database(query)
            db_obj.execute()
        """ answer store here """

        answer_dict = self.data['answer_dict']

        for i in answer_dict:

            query = f"select id from user where so_user_id = ?", (answer_dict[i]["ans_user_id"],)
            db_obj = database(query)
            y = db_obj.execute()

            if len(y) == 0:

                query = f"INSERT INTO user (so_user_id,name,rep_score,bronze,silver,gold) values(?,?,?,?,?,?)", (answer_dict[i]["ans_user_id"],answer_dict[i]["ans_user_name"],answer_dict[i]["ans_user_rep"],answer_dict[i]["ans_bronze"],answer_dict[i]["ans_silver"],answer_dict[i]["ans_gold"])
                db_obj = database(query)
                db_obj.execute()

                query = f"select id from user where so_user_id = ?", (answer_dict[i]["ans_user_id"],)
                db_obj = database(query)
                fk_ans_user_id = db_obj.execute()[0][0]
            else:
                fk_ans_user_id = y[0][0]

            query = f"INSERT INTO answer (que_id,user_id,vote,acceptance,description,ans_time) values (?,?,?,?,?,?) ", (self.data["que_id"],fk_ans_user_id,answer_dict[i]["ans_vote_count"],answer_dict[i]["ans_res_accept"],answer_dict[i]["ans_info"],answer_dict[i]["ans_time"])
            db_obj = database(query)
            db_obj.execute()

            query = f"select id from answer ORDER BY id DESC LIMIT 1"
            db_obj = database(query)
            ans_id = db_obj.execute()[0][0]

            """ answer comment store here """

            for j in answer_dict[i]['answer_comment']:
            
                query = f"INSERT INTO answer_comment (ans_id,username,comment,comm_time) values (?,?,?,?)", (ans_id,answer_dict[i]['answer_comment'][j]['ans_comm_user'],answer_dict[i]['answer_comment'][j]['ans_comm_summary'],answer_dict[i]['answer_comment'][j]['ans_comm_time'])
                db_obj = database(query)
                db_obj.execute()