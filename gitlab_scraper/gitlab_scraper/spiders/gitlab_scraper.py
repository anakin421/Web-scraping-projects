# import scrapy 
# # from gitlab_login import GitlabLoginSpider




# class GitlabScraperSpider(scrapy.Spider):
#     name = 'gitlab_scraper'
    
    


#     def scrape_pages(self, response):

#         print("\n\n\n")
#         # print(response.url)
#         # open_in_browser(response)


#         title = response.css(".page-title::text").get().strip()
#         print(title)
#         username = response.css(".user-name::text").get().strip()
#         print(username)

#         print("\n\n\n")