'''
It will fil up the original_url.txt with aprox 100k line.
'''
import sys
import requests
from bs4 import BeautifulSoup

file1 = open('main.txt', 'r')
open("original_urls.txt", "w").close()   #empty file first
source = file1.readlines()
substring = "id="
x=0
for line in source:
	line = "https://kimcartoon.li" + line[:-1]     #removing /n from end of url (code 400 if not)
	with requests.Session() as session:
		r = session.get(line)
		soup = BeautifulSoup(r.content, "html.parser")
		#job_elements = soup.findAll("ul", {"class": "list"})
		f = open("original_urls.txt", "a")
		for a in soup.find_all('a', href=True):
			if substring in a['href']:
				#print("Found the URL:", a['href'])
				f.write(a['href'] + "\n")
				x=x+1
				sys.stdout.write("\r" + "Fetching site links: "+ str(x) + "/100000 (Aprox. 100K)") #check the id number of last uploaded cartoon episode on the site (100K aprox now)
		f.close()
sys.stdout.flush()

