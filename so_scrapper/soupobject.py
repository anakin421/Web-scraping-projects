import requests
from bs4 import BeautifulSoup


def soup_obj(URL):

	res = requests.get(URL)
	soup = BeautifulSoup(res.text, 'lxml')
	return soup,res
