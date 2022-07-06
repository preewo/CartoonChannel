import requests
from bs4 import BeautifulSoup
file1 = open('main.txt', 'w')
for x in range(272):
    x = x+1
    URL = "https://kimcartoon.li/CartoonList?page=%s" % (x)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    job_elements = soup.find_all("div", class_="item")

    for link in soup.find_all("div", class_="item"):
        result = link.find('a')
        title = result.get('href') + "\n"
        print(title)
        file1.writelines(title)
	      
file1.close()
