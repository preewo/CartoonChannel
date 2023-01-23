#!/usr/bin/env python3
import sqlite3
import json
import os
import requests
import sys
import time
from sqlite3 import Error
from bs4 import BeautifulSoup
import ffmpeg
import datetime

        
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT id,vid_link FROM Episodes WHERE vid_lenght IS NULL")
    x=0
    rows = cur.fetchall()
    biggest = len(rows)
    for row in rows:
        id_nr = str(row[0]) 
        #print(id_nr)
        url = row[1].strip()
        #print(url)
        update_vid_lenght(id_nr,url)
        x=x+1
        sys.stdout.write("\r" + "Updating cartoon details: "+ str(x) + "/" + str(biggest))
        
def update_vid_lenght(id_nr,url):
	#url='https://www.luxubu.review/v/0zldgsllzex4y52'
	quality='720p'
	suffix = url.split('/')[-1]
	response = requests.post('https://www.luxubu.review/api/source/' + suffix, {}).json()
	link = [k for k in response['data'] if quality in k['label']]
	if len(link) == 0 :
		print("WARN : Could not get %s version of " %(quality))
		link = response['data'][-1]
	else :
		link = link[0]
	quality = link['label']
	print(quality)
	link_url = link['file']
	print(link_url)
	try:
		page = requests.head(link_url,allow_redirects=True)
		page.headers.get(link_url)
		follow_link = page.url
		vid = ffmpeg.probe(follow_link)
		print(follow_link)
		time.sleep(5)
		ffmpeg_duration = vid['streams'][0]['duration']
		m = int(ffmpeg_duration.split('.')[0])/60
		convert = str(datetime.timedelta(minutes = m))
		print(convert)
		database = r"Cartoon_db.db"
		conn = create_connection(database)
		cur = conn.cursor()
		cur.execute('''UPDATE Episodes SET vid_lenght = ? ,quality = ? WHERE id = ?''', (convert,quality,id_nr))
		conn.commit()
	except:
		print('ERROR!!!!!')
		time.sleep(10)
		pass
	time.sleep(5)


def main():
    database = r"Cartoon_db.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        select_all_tasks(conn)
        sys.stdout.flush()

if __name__ == '__main__':
    main()
