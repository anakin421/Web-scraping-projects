import scrapy
from scrapy.crawler import CrawlerProcess,Crawler
from spiders.gitlab_login import GitlabLoginSpider,GitlabScraperSpider
# from spiders.gitlab_scraper import GitlabScraperSpider
import logging
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from twisted.internet import defer,reactor
from scrapy import signals
from scrapy.utils.project import get_project_settings

# process = CrawlerProcess()
# process.crawl(GitlabLoginSpider)
# process.crawl(GitlabScraperSpider)
# process.start() 






data = []

def collect_items(item, response, spider):
	data.append(item)

crawler = Crawler(GitlabLoginSpider)
crawler.signals.connect(collect_items, signals.item_scraped)

process = CrawlerProcess(get_project_settings())
process.crawl(crawler)
# process.crawl(GitlabScraperSpider)	
process.start()
process.stop()


if data[0]['loged_in']:
	parseProcess = CrawlerProcess()
	parseProcess.crawl(GitlabScraperSpider,data[0]['_gitlab_session'],data[0]['response'])


# configure_logging()
# runner = CrawlerRunner()

# @defer.inlineCallbacks
# def crawl():
#     yield runner.crawl(GitlabLoginSpider)
#     # TODO How to get the session_id?
#     # session_id = yield runner.crawl(Spider1) returns None
#     # Or adding return statement in Spider 1, actually breaks 
#     # sequential processing and program sleeps before running Spider1

#     # time.sleep(2)

#     # print(f"\n\n{session_id}\n\n")

#     yield runner.crawl(GitlabScraperSpider(session_id= session_id))
#     reactor.stop()

# crawl()
# reactor.run()