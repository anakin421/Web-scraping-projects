from bs4 import BeautifulSoup as soup
import requests


def get_proxies():

    proxy_web_site = 'https://www.sslproxies.org/'
    response = requests.get(proxy_web_site)
    html_page = response.text
    soup_page = soup(html_page, "html.parser")
    containers = soup_page.find_all("div", {"class": "table-responsive"})[0]
    ip_index = [8*k for k in range(100)]

    proxy_file = open("proxy_list.txt", "w")

    for i in ip_index:
        ip = containers.find_all("td")[i].text
        port = containers.find_all("td")[i+1].text
        https = containers.find_all("td")[i+6].text

        if https == 'yes':
            proxy = ip + ':' + port
            proxy_file.write(proxy)
            proxy_file.write("\n")


    proxy_file.close()