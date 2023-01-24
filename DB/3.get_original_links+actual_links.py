import requests
import sys
from bs4 import BeautifulSoup
file1 = open('original_urls.txt', 'r')
open("original_urls+actual_urls.txt", "w").close()
source = file1.readlines()
num_line = sum(1 for line in open('original_urls.txt'))
x=0
for request_url in source:
	request_url = "https://kimcartoon.li" + request_url
	x=x+1
	with requests.Session() as session:
		request_url = request_url[:-1]
		r = session.get(request_url)
		soup = BeautifulSoup(r.content, "html.parser")
		try:
			kiir = soup.find_all('iframe', id='mVideo')[0]['src']
			result = request_url + "||" + kiir + "\n"
		except:
			result = request_url + "|| {LINK NOT FOUND!} \n"
		#print(result)
		sys.stdout.write("\r" + "Fetching episodes/movie links: " + str(x) + "/" + str(num_line))
		f = open("original_urls+actual_urls.txt", "a")
		f.write(result)
		#print(result)
sys.stdout.flush()
