import sqlite3
conn = sqlite3.connect('Cartoon_db.db') 
import json
import os
import requests
import vlc
import math
# importing time module
import time

def db_connection():
	conn = None
	try:
		conn = sqlite3.connect('Cartoon_db.db')
	except sqlite3.error as e:
		print(e)
	return conn
	
       
media_player = vlc.MediaPlayer()
conn = db_connection()
cursor = conn.execute("SELECT * FROM Schedule")
rows = cursor.fetchall()
for row in rows:
	vid_link = row[3]
	quality='360p'
	suffix = vid_link.split('/')[-1]
	print(suffix)
	test_link = "https://www.luxubu.review/api/source/" + suffix
	print(test_link)
	response = requests.post(test_link.strip() , {}).json()
	link = [x for x in response['data'] if quality in x['label']]
	links = link[0]['file']
	print(links)
	media = vlc.Media(links)
	media_player.set_media(media)
	media_player.play()
	time.sleep(3)
	value = media_player.get_length()
	print(value)
	ss = int(math.ceil(value /1000))
	print(ss)
	time.sleep(ss)
	print("Length of the media : ")
	print(value)
	
