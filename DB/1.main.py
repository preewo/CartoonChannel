import requests
import sys
from bs4 import BeautifulSoup
file1 = open('main.txt', 'w')
animation = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
last_page = 275

for x in range(last_page):
    x = x+1    # Check for the number 275, Last page in the cartoon list on the site -1
    URL = "https://kimcartoon.li/CartoonList?page=%s" % x
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    job_elements = soup.find_all("div", class_="item")
    
    for link in soup.find_all("div", class_="item"):
        result = link.find('a')
        title = result.get('href') + "\n"
        print(title)
        sys.stdout.write("\r" + "Fetching main cartoon list: " + str(x) + "/" + str(last_page))
        file1.writelines(title)
sys.stdout.flush()	      
file1.close()
