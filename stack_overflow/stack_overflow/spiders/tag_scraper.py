import scrapy 

class tag_scraper(scrapy.Spider):

	name = "tag_scraper"
	page_number = 2
	start_urls = ['https://stackoverflow.com/tags?page=1&tab=popular']

	def parse(self,response):

		print(response.status)

		file = open('so_tages.txt', 'a')

		tags = response.css(".fd-column")

		for tag in tags:

			tagname = tag.css(".post-tag::text").get().strip()
			file.write(tagname)
			file.write("\n")

		next_page = f"https://stackoverflow.com/tags?page={tag_scraper.page_number}&tab=popular"

		if tag_scraper.page_number < 1712:
			tag_scraper.page_number += 1
			yield response.follow(next_page,callback = self.parse)

		file.close()
