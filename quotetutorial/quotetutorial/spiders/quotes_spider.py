import scrapy
from ..items import QuotetutorialItem


class quotespider(scrapy.Spider):
	name = "quotes"

	start_urls = ['http://quotes.toscrape.com/']

	def parse(self,response):

		items = QuotetutorialItem()

		all_divs_quotes = response.css('div.quote')

		for quotes in all_divs_quotes:

			title = quotes.css('span.text::text').get()

			author = quotes.css('.author::text').get()

			tag = quotes.css('a.tag::text').getall()

			items['title'] = title
			items['author'] = author
			items['tag'] = tag

			yield items

		"""
		for pagination if the here in scrapy we use the response.follow method to go to the next page
		"""

		next_page = response.css("li.next a::attr(href)").get()
		# print(next_page)

		if next_page is not None:
			yield response.follow(next_page, callback = self.parse)