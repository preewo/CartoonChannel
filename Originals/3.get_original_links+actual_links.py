import requests
from bs4 import BeautifulSoup
file1 = open('original_urls.txt', 'r')
source = file1.readlines()
for request_url in source:
	request_url = "https://kimcartoon.li" + request_url
	with requests.Session() as session:
	    request_url = request_url[:-1]
	    r = session.get(request_url)
	    soup = BeautifulSoup(r.content, "html.parser")
	    try:
	    	kiir = soup.find_all('iframe', id='mVideo')[0]['src']
	    	result = request_url + "||" + kiir + "\n"
	    except:
	    	result = request_url + "|| {LINK NOT FOUND!} \n"
	    #print(soup)
	    
	    f = open("original_urls+actual_urls.txt", "a")
	    f.write(result)
	    print(result)
