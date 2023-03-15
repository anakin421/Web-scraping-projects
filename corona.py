import requests
from bs4 import BeautifulSoup

url = 'https://www.worldometers.info/coronavirus/'

res = requests.get(url)

s = BeautifulSoup(res.text,'html.parser')

data = s.find_all("div",class_ = 'maincounter-number')

# print(data)
print(f"Total Cases: {data[0].text.strip()}")
print(f"Total Deaths: {data[1].text.strip()}")
print(f"Total Recoverd: {data[2].text.strip()}")

