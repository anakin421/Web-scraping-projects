from bs4 import BeautifulSoup
from soupobject import soup_obj
from db_connect import * 

def scraper():

    tag = input("Enter Tag: ")

    pages = page_finder(tag)

    for i in range(1,pages+1):        #here you can set range to pages to scrap desire number of pages 

        """

        this page url will give 50 available question and page in url will change according to loop simultaneously 
        
        """

        PAGE_URL = f"https://stackoverflow.com/questions/tagged/{tag}?tab=newest&page={i}&pagesize=50" #main for pagination

        soup,res = soup_obj(PAGE_URL)

        question_50 = soup.select(".question-summary")



        """ this for loop will give the info of available 50(max) questions simultaneously  """


        for questions in question_50: #50 questions for 1 page 


            q = questions.select_one('.question-hyperlink')
            # print(q['href'])

            que_href = q['href']

            que_id = q['href'].split('/')[2] #que_id

            try:
                que_title = q.text  #que_title
            except:
                que_title = None


            try:
                vote_count = questions.select_one('.vote-count-post').getText()
            except:
                vote_count = None


            try:
                views = questions.select_one('.views').attrs['title']
                view_count = views.split(" ")[0]
            except:
                view_count = None
                view = None


            try:
                answer_count = questions.select_one('.status').strong.getText()         
            except:
                answer_count = None


            que_tags = questions.select('.tags > a')
            que_tags_list = []

            for i in que_tags:
                que_tags_list.append(i.getText())


            try:
                keyword1 = que_tags_list[0]
            except:
                keyword1 = None

            try:
                keyword2 = que_tags_list[1]
            except:
                keyword2 = None

            try:
                keyword3 = que_tags_list[2]
            except:
                keyword3 = None

            try:
                keyword4 = que_tags_list[3]
            except:
                keyword4 = None

            try:
                keyword5 = que_tags_list[4]
            except:
                keyword5 = None




            user_info = questions.select_one(".user-details")

            #**************************** USER ID ******************************

            try:
                user_id = user_info.a['href'].split("/")[2]
            except:
                user_id = None


            #**************************** USER NAME ******************************

            try:
                user_name = user_info.a.getText()
            except:
                user_name = None

            #**************************** USER REPUTATION SCORE ******************************

            try:
                user_rep = user_info.select_one('.-flair > .reputation-score').getText()
            except:
                user_rep = None


            #**************************** USER BRONZE MEDAL ******************************

            try:
                bronze = user_info.select_one('span > .badge3').next_sibling.getText()
            except:
                bronze = None

            #**************************** USER SILVER MEDAL ******************************

            try:
                silver = user_info.select_one('span > .badge2').next_sibling.getText()
            except:
                silver = None

            #**************************** USER GOLD MEDAL ******************************

            try:
                gold = user_info.select_one('span > .badge1').next_sibling.getText()
            except:
                gold = None



            """ user info will store here """

            query = f"select id from user where so_user_id = ?", (user_id,)
            db_obj = database(query)
            x = db_obj.execute()

            if len(x) == 0:

                query1 = f"INSERT INTO user (so_user_id,name,rep_score,bronze,silver,gold) values(?,?,?,?,?,?)", (user_id,user_name,user_rep,bronze,silver,gold)
                db_obj1 = database(query1)
                db_obj1.execute()

                query2 = f"select id from user where so_user_id = ?", (user_id,)
                db_obj2 = database(query2)
                u_id = db_obj2.execute()

                fk_user_id = u_id[0][0]

            else:

                fk_user_id = x[0][0]




            """
                
            NOW FROM HERE ON WE'RE GOING ON PARTICULAR QUESTION'S URL   

            """


            QUE_URL = f"https://stackoverflow.com/questions/{que_id}" #question URL
            # QUE_URL = f"https://stackoverflow.com{que_href}" #question URL

            soup1,res1 = soup_obj(QUE_URL)

            if len(res1.history) == 2:
                continue

            #**************************** QUESTION TIME *****************************

            try:
                que_time = soup1.select_one('time[itemprop="dateCreated"]')['datetime'] #que_time 
            except:
                que_time = None



            #**************************** QUESTION DESCRIPTION *****************************

            try:
                question = soup1.select_one(".question")
                que_summary  = question.select_one(".post-text")
            except:
                continue

            try:
                aside_tag = que_summary.aside
                aside_tag.decompose()
            except:
                pass

            try:    
                ques_summary = que_summary.getText()
            except:
                ques_summary = None



            """ question info will store here for question table  """

            query = f"select id from question where id = ?", (que_id,)
            db_obj = database(query)
            q_id = db_obj.execute()

            if len(q_id) == 0:

                query1 = f"INSERT INTO question (id,title,view_count,vote,total_ans,description,que_time,user_id,keyword1,keyword2,keyword3,keyword4,keyword5) values(?,?,?,?,?,?,?,?,?,?,?,?,?)", (que_id,que_title,view_count,vote_count,answer_count,ques_summary,que_time,fk_user_id,keyword1,keyword2,keyword3,keyword4,keyword5)
                db_obj1 = database(query1)
                db_obj1.execute()               

            else:
                print(f"******************************************************* question id {que_id} is already stored **********************************************")
                continue

            """
                
            THIS FOR LOOP WILL SCRAP THE VARIOUS COMMENTS FROM 1 QUESTION   

            """

            print(f"question id {que_id} ---> scraped")


            comments = question.select(".comments-list > .comment")

            if len(comments):

                for comm in comments:

                    try:
                        comm_summary = comm.select_one(".comment-copy").getText()
                    except:
                        comm_summary = None

                    try:
                        comm_user = comm.select_one(".comment-user").getText()
                    except:
                        comm_user = None

                    try:
                        comm_date = comm.select_one('.relativetime-clean')['title']
                    except:
                        comm_date = None



                    query = f"INSERT INTO question_comment (que_id,username,comment,comm_time) values (?,?,?,?)", (que_id,comm_user,comm_summary,comm_date)
                    db_obj = database(query)
                    db_obj.execute()

            else:
                # print("No comments")
                pass




            """
                
            THIS IS THE ANSWER SECTION FOR 1 QUESTION. IT WILL SCRAP ALL RHE AVAILABLE ANSWER ONE AFTER ONE     

            """



            answers = soup1.select("#answers > .answer")

            if len(answers):
                for ans in answers:

                    try:
                        ans_vote_count = ans.select_one(".js-vote-count").getText()
                    except:
                        ans_vote_count = None


                    ans_accept = ans.select_one("div > .js-accepted-answer-indicator")['class']

                    try:
                        if "d-none" in ans_accept:
                            ans_res_accept = 'Not Accpeted'
                        else:
                            ans_res_accept = 'Accpeted'
                    except:
                        ans_res_accept = None

                    try:
                        ans_info = ans.select_one(".post-text").getText()
                    except:
                        ans_info = None


                    """ ------------- ANSWER GIVEN BY USER INFORMATION ---------------"""

                    try:
                        ans_user_id = ans.select_one(".user-details > a")['href'].split('/')[2]

                    except:
                        ans_user_id = None

                    try:
                        ans_user_name = ans.select_one(".user-details > a").getText().strip()
                    except:
                        ans_user_name = None

                    try:
                        ans_user_rep = ans.select_one('.-flair > .reputation-score').getText()
                    except:
                        ans_user_rep = None

                    try:
                        ans_bronze = ans.select_one('span > .badge3').next_sibling.getText()
                    except:
                        ans_bronze = None

                    try:
                        ans_silver = ans.select_one('span > .badge2').next_sibling.getText()
                    except:
                        ans_silver = None

                    try:
                        ans_gold = ans.select_one('span > .badge1').next_sibling.getText()
                    except:
                        ans_gold = None

                    try:
                        ans_date = ans.select_one(".relativetime")['title']
                    except:
                        ans_date = None




                    """ user info of the answer will store here """

                    query = f"select id from user where so_user_id = ?", (ans_user_id,)
                    db_obj = database(query)
                    y = db_obj.execute()

                    if len(y) == 0:

                        query1 = f"INSERT INTO user (so_user_id,name,rep_score,bronze,silver,gold) values(?,?,?,?,?,?)", (ans_user_id,ans_user_name,ans_user_rep,ans_bronze,ans_silver,ans_gold)
                        db_obj1 = database(query1)
                        db_obj1.execute()


                        query2 = f"select id from user where so_user_id = ?", (ans_user_id,)
                        db_obj2 = database(query2)
                        u_ans_id = db_obj2.execute()

                        fk_ans_user_id = u_ans_id[0][0]

                    else:

                        fk_ans_user_id = y[0][0]



                    query = f"INSERT INTO answer (que_id,user_id,vote,acceptance,description,ans_time) values (?,?,?,?,?,?) ", (que_id,fk_ans_user_id,ans_vote_count,ans_res_accept,ans_info,ans_date)
                    db_obj = database(query)
                    db_obj.execute()


                    query1 = f"select id from answer ORDER BY id DESC LIMIT 1"
                    db_obj1 = database(query1)
                    a_id = db_obj1.execute()

                    ans_id = a_id[0][0]

                    """
                
                    THIS FOR LOOP WILL SCRAP THE VARIOUS COMMENTS FROM 1 ANSWER IF IT'S AVAILABLE   

                    """


                    comments = ans.select(".comments-list > .comment")

                    if len(comments):

                        for comm in comments:
                            try:
                                ans_comm_summary = comm.select_one(".comment-copy").getText()
                            except:
                                ans_comm_summary = None

                            try:
                                ans_comm_user = comm.select_one(".comment-user").getText()
                            except:
                                ans_comm_user = None

                            try:
                                ans_comm_date = comm.select_one('.relativetime-clean')['title']
                            except:
                                ans_comm_date = None


                            query = f"INSERT INTO answer_comment (ans_id,username,comment,comm_time) values (?,?,?,?)", (ans_id,ans_comm_user,ans_comm_summary,ans_comm_date)
                            db_obj = database(query)
                            db_obj.execute()


                    else:
                        # print("No comments")
                        pass

            else:
                # print("No answers")
                pass




def page_finder(tag):


    """
    
    this function will find the total number's of page that are available in the stack overflow for desire tag.. but as of 
    now it is set the max 5 page for 1 tag.. and if the tag has less number of pages than that then it'll consider those amount 
    of pages to scrap.. and also it'll check given keyword is valid or not by checking the all available keywords in stack overflow
    via earlier created tags.txt file

    """


    with open('tags.txt','r') as f:
        tag_list = f.readlines()

    tag_elem = f"{tag}\n"

    if tag_elem.lower() in tag_list:

        TAG_URL = f"https://stackoverflow.com/questions/tagged/{tag}"

        total_page,r = soup_obj(TAG_URL)

        try:
            max_page_no = int(total_page.select(".pager > a")[-2].getText())

        except IndexError:
            max_page_no = 1

        if max_page_no > 5:    #here you can set as much as pages but for now it's upto 5 pages
            pages = 5
        else:
            pages = max_page_no

    else:
        print("Sorry!! This tag is not available in stack overflow")
        exit()

    return pages


if __name__=='__main__':
    scraper()