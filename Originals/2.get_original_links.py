import requests
from bs4 import BeautifulSoup
payload = {
    'username': 'woopang',
    'pass': 'eminem20'
}
post_login = "https://kimcartoon.li/Login"
file1 = open('myfile.txt', 'r')
source = file1.readlines()
substring = "id="
for line in source:
	line = "https://kimcartoon.li" + line[:-1]     #removing /n from end of url (code 400 if not)
	with requests.Session() as session:
		post = session.post(post_login, data=payload)
		r = session.get(line)
		soup = BeautifulSoup(r.content, "html.parser")
		#job_elements = soup.findAll("ul", {"class": "list"})
		f = open("original_urls.txt", "a")
		for a in soup.find_all('a', href=True):
			if substring in a['href']:
				print("Found the URL:", a['href'])
				f.write(a['href'] + "\n")
		f.close()
					

		#print(job_elements)   #or whatever else you want to do with the request data!
