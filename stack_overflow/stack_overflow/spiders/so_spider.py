import scrapy
from ..items import StackOverflowItem
from ..proxies import get_proxies

class so_spider(scrapy.Spider):
    name = "so_spider"
    tag = input("enter tag: ")

    with open("/home/abhishek/abhishek/scrapping/stack_overflow/so_tages.txt","r") as f:
        tag_list = f.readlines()

    tag_elem = f"{tag}\n"

    if tag_elem.lower() not in tag_list:  #if the given input is not in the stack overflow keywords it'll exit the code
        print("Sorry!! This tag is not available in stack overflow")
        exit()

    # get_proxies()
    start_urls = [f"https://stackoverflow.com/questions/tagged/{tag}"]


    def parse(self,response):

        # print(response.status)
        try:
            max_page_no = int(response.css(".pager > a::text").getall()[-2])
        except IndexError:
            max_page_no = 1

        pages = 5 if max_page_no > 5 else max_page_no

        for i in range(1,pages+1):
            PAGE_URL = f"https://stackoverflow.com/questions/tagged/{so_spider.tag}?tab=newest&page={i}&pagesize=50"

            yield response.follow(PAGE_URL,callback = self.parse_questions)

    
    def parse_questions(self,response):

        """
        this method will generate the 50 various question links and yield it simultensouly  
        """


        que_50_list = response.css("#questions .question-hyperlink::attr(href)").getall()

        for TEMP_QUE_URL in que_50_list: 

            QUE_URL = f'https://stackoverflow.com{TEMP_QUE_URL}'

            yield response.follow(QUE_URL, callback = self.questions_info)


    def questions_info(self,response):

        """
        this method will scrap all the available information of each question
        """

        item = StackOverflowItem()

        que_url = response.url

        que_id = que_url.split("/")[4]

        que_title = response.css("#question-header .question-hyperlink::text").get()

        view_count = response.css(".mb8~ .mb8+ .mb8 ::attr(title)").get().split(" ")[1]

        vote_count = response.css("#question .ai-center::text").get()

        que_time = response.css("time ::attr(datetime)").get()

        que_tags_list = response.css("#question .post-tag::text").getall()
        
        keyword1 = que_tags_list[0]

        try:
            keyword2 = que_tags_list[1]
        except IndexError:
            keyword2 = None

        try:
            keyword3 = que_tags_list[2]
        except IndexError:
            keyword3 = None

        try:
            keyword4 = que_tags_list[3]
        except IndexError:
            keyword4 = None

        try:
            keyword5 = que_tags_list[4]
        except IndexError:
            keyword5 = None

        try:
            user_id = response.css("#question .user-details a::attr(href)").get().split("/")[2]
        except AttributeError:
            user_id = 0

        try:
            user_name = response.css("#question .user-details a::text").get().strip()
        except:
            user_name = 'unknown'

        user_rep = response.css("#question .reputation-score::text").get()

        bronze = response.css("#question .badge3+ .badgecount::text").get()

        silver = response.css("#question .badge2+ .badgecount::text").get()

        gold = response.css("#question .badge1+ .badgecount::text").get()

        que_summary = response.css("#question .post-text ::text").getall()
        que_summary = "".join([i for i in que_summary if i.strip() != ''])  

        answer_count = response.css("#answers-header .mb0::attr(data-answercount)").get()



        # print("\n\n\n******************************************************\n")
        # print(f"que_id : {que_id}")
        # print(f"que_title : {que_title}")
        # print(f"vote_count : {vote_count}")
        # print(f"view_count : {view_count}")
        # print(f"que_time : {que_time}")
        # print(f"\nque_summary : {que_summary}")
        # print(f"\nuser_id : {user_id}")
        # print(f"user name : {user_name}")
        # print(f'user rep : {user_rep}')
        # print(f"bronze : {bronze}")
        # print(f"silver : {silver}")
        # print(f"gold : {gold}")
        # print(f"tags : {que_tags_list}")
        # print(f"answer_count : {answer_count}")





        #-------------------question comment section------------------------------

        ques_comm_dict = dict()

        comments = response.css(".question .comments-list > .comment")

        que_comm_count = 1

        if len(comments):

            for comm in comments:

                comm_summary = comm.css(".comment-copy ::text").getall()
                comm_summary = "".join(comm_summary)

                comm_user = comm.css(".comment-user::text").get()

                comm_time = comm.css(".relativetime-clean::attr(title)").get()


                ques_comm_dict[f"{que_comm_count}"] = dict(comm_summary = comm_summary, comm_user = comm_user, comm_time = comm_time)  
                que_comm_count += 1


        # print(f"question comments : {ques_comm_dict}")


        #-----------------------------answer section-------------------------------

        answer_dict = dict()

        ans_count = 1

        answers = response.css("#answers > .answer")

        if len(answers):
            for ans in answers:

                ans_vote_count = ans.css(".fd-column.ai-center::text").get()

                ans_accept = ans.css("div > .js-accepted-answer-indicator").xpath("@class").getall()

                if "d-none" in ans_accept[0]:
                    ans_res_accept = 'Not Accpeted'
                else:
                    ans_res_accept = 'Accpeted'

                ans_info = ans.css(".post-text ::text").getall()
                ans_info = "".join(ans_info)

                """ ------------- ANSWER GIVEN BY USER INFORMATION ---------------"""


                # ans_user = ans.css(".user-details a").getall()

                if ans.css(".user-details::attr(itemprop)").get() == 'author':
                    try:
                        ans_user_id = ans.css(".user-details a::attr(href)").get().split("/")[2]
                    except AttributeError:
                        ans_user_id = 0

                    try:
                        ans_user_name = ans.css(".user-details > a::text").get().strip()
                    except AttributeError:
                        ans_user_name = "unknown"

                else: 
                    try:
                        ans_user_id = ans.css(".user-details a:last-child::attr(href)").get().split("/")[2]
                    except AttributeError:
                        ans_user_id = 0

                    try:
                        ans_user_name = ans.css(".user-details  a:last-child::text").get().strip()
                    except AttributeError:
                        ans_user_name = 'unknown'

                ans_user_rep = ans.css('.reputation-score::text').get()

                ans_bronze = ans.css(".badge3+ .badgecount::text").get()

                ans_silver = ans.css(".badge2+ .badgecount::text").get()

                ans_gold = ans.css(".badge1+ .badgecount::text").get()

                ans_time = ans.css(".relativetime::attr(title)").get()


                """
            
                THIS FOR LOOP WILL SCRAP THE VARIOUS COMMENTS FROM 1 ANSWER IF IT'S AVAILABLE   

                """

                ans_comm_dict = dict()
                ans_comm_count = 1

                ans_comments = ans.css(".comments-list > .comment")

                if len(ans_comments):

                    for ans_comm in ans_comments:

                        ans_comm_summary = ans_comm.css(".comment-copy ::text").getall()
                        ans_comm_summary = "".join(ans_comm_summary)

                        ans_comm_user = ans_comm.css(".comment-user::text").get()

                        ans_comm_time = ans_comm.css(".relativetime-clean::attr(title)").get()


                        ans_comm_dict[f"{ans_comm_count}"] = dict(ans_comm_summary = ans_comm_summary, ans_comm_user = ans_comm_user, ans_comm_time = ans_comm_time) 
                        ans_comm_count += 1


                answer_dict[f"{ans_count}"] = dict(ans_vote_count = ans_vote_count,ans_res_accept = ans_res_accept,ans_info = ans_info,ans_user_id = ans_user_id,ans_user_name = ans_user_name,ans_user_rep = ans_user_rep,ans_bronze = ans_bronze,ans_silver = ans_silver,ans_gold = ans_gold,ans_time = ans_time,answer_comment = ans_comm_dict)
                ans_count += 1


        # print(f"\nanswer info : {answer_dict}")
        # print("\n\n\n")


        item['que_id'] = que_id
        item["que_title"] = que_title
        item['vote_count'] = vote_count
        item["view_count"] = view_count
        item['que_summary'] = que_summary
        item["que_time"] = que_time
        item['keyword1'] = keyword1
        item['keyword2'] = keyword2
        item['keyword3'] = keyword3
        item['keyword4'] = keyword4
        item['keyword5'] = keyword5

        item["answer_count"] = answer_count

        item['user_id'] = user_id
        item['user_name'] = user_name
        item['user_rep'] = user_rep
        item['bronze'] = bronze
        item['silver'] = silver
        item['gold'] = gold


        item['ques_comm_dict'] = ques_comm_dict

        item['answer_dict'] = answer_dict


        yield item
