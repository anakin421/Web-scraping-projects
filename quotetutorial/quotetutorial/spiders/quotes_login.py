# import scrapy 
# from scrapy.http import FormRequest
# from scrapy.utils.response import open_in_browser


# class LoginSpider(scrapy.Spider):
#     name = 'quoteslogin'
#     start_urls = ['http://quotes.toscrape.com/login']

#     def parse(self, response):
#         token = response.css('form input::attr(value)').get()
#         return FormRequest.from_response(response,
#                                          formdata={'csrf_token': token,
#                                                    'password': 'foobar',
#                                                    'username': 'foobar'},
#                                          callback=self.scrape_pages)


#     def scrape_pages(self, response):
#         open_in_browser(response)



import scrapy 
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


# class LoginSpider(scrapy.Spider):
#     name = 'sologin'

#     allowed_domains = ["stackoverflow.com"]
#     start_urls = ['https://stackoverflow.com/users/login']

#     def parse(self, response):
#         fkey = response.css('#login-form input::attr(value)').get().strip()

#         print("\n\n\n")


#         # print(response.url)
#         print(fkey)


#         # "oauth_version": ""
#         # "oauth_server": ""

#         return FormRequest.from_response(response,
#                                          formdata={'fkey': fkey,
#                                                     'ssrc' : 'login',
#                                                    'email': 'abhisatasiya123@gmail.com',
#                                                    'password': 'Q1w2e3r4t5y6@'                                                                 
#                                                     },dont_click = True,
#                                          callback=self.scrape_pages)


#     def scrape_pages(self, response):

#         print("\n\n\n")
#         print(response.url)
#         open_in_browser(response)
#         print("\n\n\n")

#         # print(response.text)



class LoginSpider(scrapy.Spider):
    name = 'gitlogin'

    allowed_domains = ["gitlab.com"]
    start_urls = ['https://gitlab.com/users/sign_in']

    def parse(self, response):
        authenticity_token = response.css('meta[name="csrf-token"]::attr(content)').get().strip()



        # print(response.url)
        print()
        print(authenticity_token)
        print()

        # "oauth_version": ""
        # "oauth_server": ""

        return FormRequest.from_response(response,
                                         formdata={'authenticity_token': authenticity_token,
                                                    'user[login]' : 'example@gmail.com',
                                                   'user[password]': 'Q1w2e3r4t5y6@',
                                                   'user[remember_me]': '0'                                                                 
                                                    },dont_click = True,
                                         callback=self.scrape_pages)

    def scrape_pages(self, response):

        print("\n\n\n")
        # print(response.url)
        # open_in_browser(response)


        title = response.css(".page-title::text").get().strip()
        print(title)
        username = response.css(".user-name::text").get().strip()
        print(username)

        print("\n\n\n")

        # print(response.text)        