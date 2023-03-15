# -*- coding: utf-8 -*-
import scrapy 
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from scrapy.crawler import CrawlerProcess
from scrapy.http.cookies import CookieJar



# from gitlab_scraper.spiders.gitlab_scraper import GitlabLoginSpider


class GitlabLoginSpider(scrapy.Spider):
    name = 'gitlab_login'
    allowed_domains = ['gitlab.com']
    start_urls = ['https://gitlab.com/users/sign_in']

    def parse(self, response):
        authenticity_token = response.css('meta[name="csrf-token"]::attr(content)').get().strip()

        # cookieJar = response.meta.setdefault('cookie_jar', CookieJar())
        # cookieJar.extract_cookies(response, response.request)
        # cookieJar.add_cookie_header(response.request) # apply Set-Cookie ourselves

        # print(f"cookieJar:  {cookieJar}")


        yield FormRequest.from_response(response,
                                         formdata={'authenticity_token': authenticity_token,
                                                    'user[login]' : 'Example@gmail.com',
                                                   'user[password]': 'Q1w2e3r4t5y6@',
                                                   'user[remember_me]': '0'                                                                 
                                                    },dont_click = True, dont_filter=True,
                                         callback=self.afterlogin)



    def afterlogin(self, response):


        if response.css(".sign-out-link::text").get() == 'Sign out':
            print("\n------successfully loged in !!-----\n")

            # print(response.request.url)
            # print(response.url)

            # print(response.headers.getlist('Cookie'))


            link = response.css(".header-user-dropdown-toggle::attr(href)").get()
            user_link = f"https://gitlab.com{link}"
            # print(user_link)

            # print(type(response.headers))
            # print(response.headers.getlist("Set-Cookie"))
            x  = response.request.headers.getlist("Cookie")
            # print(x)
            # print(response.headers.getlist("Set-Cookie"))

            sessionid = str(str(x[0]).split("_gitlab_session=")[1]).split(";")[0]


            session_id = dict(_gitlab_session  = sessionid,loged_in = True,response = response)

            # print(response.request.headers)

            # yield response.follow(url=user_link,callback = GitlabScraperSpider.parse, meta = {'response':user_link})
            return session_id

            # request = scrapy.Request(response.request.url,
            #                          callback=GitlabScraperSpider.parse)
            # request.meta['response'] = response
            # yield request

        else:
            print("-----login failed-----")


        # print("\n\n\n")
        # # print(response.url)
        # # open_in_browser(response)


        # title = response.css(".page-title::text").get().strip()
        # print(title)
        # username = response.css(".user-name::text").get().strip()
        # print(username)
        # link = response.css(".header-user-dropdown-toggle::attr(href)").get()
        # print(f"https://gitlab.com{link}")
        # print("\n\n\n")


class GitlabScraperSpider(scrapy.Spider):
    name = 'gitlab_scraper'

    def __init__(self, session_id,response):
        self.session_id = session_id
        self.response = response
        print(f"*******************{self.session_id}**************************")
        print(f"*******************{self.response.url}**************************")


    # start_urls = ['https://gitlab.com']


    def start_requests(self):

        request = scrapy.Request('https://gitlab.com',cookies = self.session_id,
                                 callback=self.scrape_info)
        # request.meta['response'] = response
        yield request


    # def parse(self,response):



    def scrape_info(self, response):

        print("\n\n\n")
        print(response.url)
        # open_in_browser(response)
        # new_response = response.meta['response']
        # print(new_response)

        title = response.css(".page-title::text").get().strip()
        print(title)
        username = response.css(".user-name::text").get().strip()
        print(username)

        print("\n\n\n")




# process = CrawlerProcess()

# process.crawl(GitlabLoginSpider )
# process.start()