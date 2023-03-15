import requests
from bs4 import BeautifulSoup


def tag_scraper():   # it's store all the available tags of stack overflow in tages.txt file  

	MAIN_TAG_URL = f"https://stackoverflow.com/tags"

	res = requests.get(MAIN_TAG_URL)

	soupobj = BeautifulSoup(res.text, 'lxml')
	max_page_num  = int(soupobj.select(".pager > a")[-2].getText())

	file = open('tags.txt','w')

	for i in range(1,max_page_num+1): #add max_page_num

		TAG_FIND_URL = f'https://stackoverflow.com/tags?page={i}&tab=popular'

		res1 = requests.get(TAG_FIND_URL)
		soupobj1 = BeautifulSoup(res1.text, 'lxml')

		for i in soupobj1.select("#tags-browser > .s-card"):

			tag_name = i.select_one(".s-card > .grid ").getText().strip()

			file.write(tag_name)
			file.write("\n")

	file.close()


tag_scraper()