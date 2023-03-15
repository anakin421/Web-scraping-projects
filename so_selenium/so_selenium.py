from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium. common. exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from db_add_data import add_data


class scraper():

    def __init__(self,tag):
        self.tag = tag

    def check_tag(self):
        with open("/home/abhishek/abhishek/selenium/so_selenium/so_tages.txt","r") as f:
            tag_list = f.readlines()
        tag_elem = f"{self.tag}\n"

        if tag_elem.lower() not in tag_list:  #if the given input is not in the stack overflow keywords it'll exit the code
            print("Sorry!! This tag is not available in stack overflow")
            exit()

        else:
            self.scraper()


    def scraper(self):

        chromedriver = "/home/abhishek/chromedriver"
        driver = webdriver.Chrome(chromedriver)
        driver.maximize_window()
        wait = WebDriverWait(driver, 30)

        driver.get("https://stackoverflow.com/tags")

        tag_elem = driver.find_element_by_xpath("//*[@id='tagfilter']")
        tag_elem.send_keys(tag)

        data = dict()

        try:
            wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'post-tag'),tag))
        except TimeoutException:
            print("timeout !!")
            driver.close()
            exit()

        driver.find_element_by_xpath("//*[@id='tags-browser']/div[1]/div[1]/div/a").click()

        print(f"\n\n{driver.current_url}\n\n")

        try:
            max_pages_no = int(driver.find_elements_by_css_selector('.pager .s-pagination--item')[-2].text)
        except IndexError:
            max_pages_no = 1


        PAGES = 2 if max_pages_no > 2 else max_pages_no

        COUNT = 1

        while True:

            questions = driver.find_elements_by_css_selector(".question-summary")

            que_list = [que.find_element_by_css_selector(".question-hyperlink").get_attribute("href") for que in questions]

            for que_link in range(len(que_list)):
                
                print(que_list[que_link])
                driver.get(que_list[que_link])

                data['vote_count'] = driver.find_element_by_css_selector("#question .ai-center").text

                data["que_time"] = driver.find_element_by_css_selector("time").get_attribute("datetime")

                que_url = driver.current_url

                data['que_id'] = que_url.split("/")[4]

                data["que_title"] = driver.find_element_by_css_selector("#question-header .question-hyperlink").text

                data["view_count"] = driver.find_element_by_css_selector(".mb8~ .mb8+ .mb8").get_attribute('title').split(" ")[1]

                que_tags_list = driver.find_elements_by_css_selector("#question .post-tag")
                que_tag_list = [que_tag.text for que_tag in que_tags_list]

                data["keyword1"] = que_tag_list[0]

                try:
                    data["keyword2"] = que_tag_list[1]
                except IndexError:
                    data["keyword2"] = None

                try:
                    data["keyword3"] = que_tag_list[2]
                except IndexError:
                    data["keyword3"] = None

                try:
                    data["keyword4"] = que_tag_list[3]
                except IndexError:
                    data["keyword4"] = None

                try:
                    data["keyword5"] = que_tag_list[4]
                except IndexError:
                    data["keyword5"] = None


                data["que_summary"] = driver.find_element_by_css_selector("#question .post-text").text

                data["answer_count"] = driver.find_element_by_css_selector("#answers-header .mb0").get_attribute("data-answercount")

                data["user_id"] = driver.find_element_by_css_selector("#question .user-details a").get_attribute('href').split("/")[4]

                data["user_name"] = driver.find_element_by_css_selector("#question .user-details a").text

                try:
                    data["user_rep"] = driver.find_element_by_css_selector("#question .reputation-score").text
                except NoSuchElementException:
                    data["user_rep"] = None

                try:
                    data["user_bronze"] = driver.find_element_by_css_selector('#question .badge3+ .badgecount').text
                except NoSuchElementException:
                    data["user_bronze"] = None

                try:
                    data["user_silver"] = driver.find_element_by_css_selector('#question .badge2+ .badgecount').text
                except NoSuchElementException:
                    data["user_silver"] = None

                try:
                    data["user_gold"] = driver.find_element_by_css_selector('#question .badge1+ .badgecount').text
                except NoSuchElementException:
                    data["user_gold"] = None


                que_comments = driver.find_elements_by_css_selector('#question .comment-body') 
                data["ques_comm_dict"] = dict()
                que_comm_count = 1

                for comm in que_comments:
                    comm_summary = comm.find_element_by_css_selector(".comment-copy").text
                    comm_user = comm.find_element_by_css_selector(".comment-user").text
                    comm_time = comm.find_element_by_css_selector(".relativetime-clean").get_attribute("title")
                    
                    data['ques_comm_dict'][f"{que_comm_count}"] = dict(comm_summary = comm_summary, comm_user = comm_user, comm_time = comm_time)  
                    que_comm_count += 1

                # print(data['ques_comm_dict'])

                # print(f"que_id: {data['que_id']}")
                # print(f"vote_count: {data['vote_count']}")
                # print(f"vote_count: {data['vote_count']}")
                # print(f"que_time: {data['que_time']}")
                # print(f"que_title: {data['que_title']}")
                # print(f"view_count: {data['view_count']}")
                # print(que_tag_list)
                # print(f"que_summary: {data['que_summary']}")
                # print(f"answer_count: {data['answer_count']}")
                # print(f"user_id: {data['user_id']}")
                # print(f"user_name: {data['user_name']}")
                # print(f"user_rep: {data['user_rep']}")
                # print(f"bronze: {data['user_bronze']}")
                # print(f"silver: {data['user_silver']}")
                # print(f"gold: {data['user_gold']}")




                answers = driver.find_elements_by_css_selector("#answers .answer")

                # print("\n ------------ answer----------------\n")

                data["answer_dict"] = dict()
                ans_count = 1

                for ans in answers:
                    ans_vote_count = ans.find_element_by_css_selector(".fd-column.ai-center").text

                    ans_accept = ans.find_element_by_css_selector(".js-accepted-answer-indicator").get_attribute('class')
                    # print(ans_accept)

                    if "d-none" in ans_accept:
                        ans_res_accept = 'Not Accpeted'
                    else:
                        ans_res_accept = 'Accpeted'


                    ans_time = ans.find_element_by_css_selector(".relativetime").get_attribute("title")

                    ans_info = ans.find_element_by_css_selector(".post-text").text

                    try:
                        ans_user_id = ans.find_element_by_css_selector(".user-details a").get_attribute('href').split("/")[4]
                    except NoSuchElementException:
                        ans_user_id = 0

                    try:
                        ans_user_name = ans.find_element_by_css_selector(".user-details > a").text
                    except NoSuchElementException:
                        ans_user_name = 'unknown'

                    try:
                        ans_user_rep = ans.find_element_by_css_selector(".reputation-score").text
                    except NoSuchElementException:
                        ans_user_rep = None


                    try:
                        ans_user_bronze = ans.find_element_by_css_selector('.badge3+ .badgecount').text
                    except NoSuchElementException:
                        ans_user_bronze = None

                    try:
                        ans_user_silver = ans.find_element_by_css_selector('.badge2+ .badgecount').text
                    except NoSuchElementException:
                        ans_user_silver = None

                    try:
                        ans_user_gold = ans.find_element_by_css_selector('.badge1+ .badgecount').text
                    except NoSuchElementException:
                        ans_user_gold = None


                    # print(f"ans_vote_count: {ans_vote_count}")
                    # print(f"ans_res_accept: {ans_res_accept}")
                    # print(f"ans_info: {ans_info}")
                    # print(f"ans_time: {ans_time}")
                    # print(f"ans_user_id: {ans_user_id}")
                    # print(f"ans_user_name: {ans_user_name}")
                    # print(f"ans_user_rep: {ans_user_rep}")
                    # print(f"ans_user_bronze: {ans_user_bronze}")
                    # print(f"ans_user_silver: {ans_user_silver}")
                    # print(f"ans_user_gold: {ans_user_gold}")


                    ans_comments = ans.find_elements_by_css_selector('.comment-body') 

                    ans_comm_dict = dict()
                    ans_comm_count = 1

                    for comm in ans_comments:
                        ans_comm_summary = comm.find_element_by_css_selector(".comment-copy").text
                        ans_comm_user = comm.find_element_by_css_selector(".comment-user").text
                        ans_comm_time = comm.find_element_by_css_selector(".relativetime-clean").get_attribute("title")

                        ans_comm_dict[f"{ans_comm_count}"] = dict(ans_comm_summary = ans_comm_summary, ans_comm_user = ans_comm_user, ans_comm_time = ans_comm_time) 
                        ans_comm_count += 1

                    data['answer_dict'][f"{ans_count}"] = dict(ans_vote_count = ans_vote_count,ans_res_accept = ans_res_accept,ans_info = ans_info,ans_user_id = ans_user_id,ans_user_name = ans_user_name,ans_user_rep = ans_user_rep,ans_bronze = ans_user_bronze,ans_silver = ans_user_silver,ans_gold = ans_user_gold,ans_time = ans_time,answer_comment = ans_comm_dict)
                    ans_count += 1

                # print(data["answer_dict"])

                print("************************************************************************")



                # data['que_id'] = que_id
                # data["que_title"] = que_title
                # data['vote_count'] = vote_count
                # data["view_count"] = view_count
                # data['que_summary'] = que_summary
                # data["que_time"] = que_time
                # data['keyword1'] = keyword1
                # data['keyword2'] = keyword2
                # data['keyword3'] = keyword3
                # data['keyword4'] = keyword4
                # data['keyword5'] = keyword5
                # data["answer_count"] = answer_count
                # data['user_id'] = user_id
                # data['user_name'] = user_name
                # data['user_rep'] = user_rep
                # data['user_bronze'] = user_bronze
                # data['user_silver'] = user_silver
                # data['user_gold'] = user_gold
                # data['ques_comm_dict'] = ques_comm_dict
                # data['answer_dict'] = answer_dict

                add = add_data(data)
                add.check_duplication()


            COUNT += 1
            if COUNT > PAGES:
                break
            else:
                print("\n+++++++++++++++++++ new page +++++++++++++++++++++\n")
                driver.get(f"https://stackoverflow.com/questions/tagged/{self.tag}?tab=newest&page={COUNT}&pagesize=15")

        driver.close()

if __name__=='__main__':
    tag = input("enter tag name: ").strip()
    scrap_obj = scraper(tag)
    scrap_obj.check_tag()