import sqlite3
import requests
import sys
from bs4 import BeautifulSoup
from sqlite3 import Error

def update_database(database_list):
#	print(database_list)
	id_nr = database_list[0]
	url = database_list[1]
	genre = database_list[2]
	poster = database_list[3]
	date = database_list[4]
	status = database_list[5]
	summary = database_list[6]
	database = r"Cartoon_db.sqlite"
	conn = create_connection(database)
	cur = conn.cursor()
	cur.execute('''UPDATE Main_Cartoons SET date_aired = ? ,status = ?, summary = ?,genre = ?,poster_url = ? WHERE id = ?''', (date,status,summary,genre,poster,id_nr))
	conn.commit()
	
def get_details(url,id_nr):
	database_list = []
	date_int=1
	status_int=2
	summary_int=4
	database_list.append(id_nr)
	database_list.append(url)
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")
	###     COLLECTING CARTOON GENRE ###
	job_elements = soup.find_all("a", class_="dotUnder")
	l = []
	for i in job_elements:
		genre = i['href'].split("/")[2]
		l.append(genre)
	final_genre = ','.join(l)
	database_list.append(final_genre)
	###     COLLECTING CARTOON POSTER ###
	job_elements = soup.find_all("img")
	final_poster = job_elements[0]['src']
	if not final_poster.startswith("http://") and not final_poster.startswith("https://"):
		final_poster = "https://kimcartoon.li" + final_poster
	database_list.append(final_poster)
	#print(url + "       ||||||||||         https://kimcartoon.li" + job_elements[0]['src'])
	###     COLLECTING CARTOON DATE AIRED ###
	check_element = soup.find_all("p")[0]
	check_if_othername = str(check_element).split(">")[2].split("<")[0][:-1].strip()
	if check_if_othername == 'Other name':
		date_int=2
		status_int=3
		summary_int=5
	job_elements = soup.find_all("p")[date_int]
	final_date = str(job_elements).split(">")[3][:-10].strip()
	database_list.append(final_date)
	#print(final_date)
	###     COLLECTING CARTOON STATUS###
	
	job_elements = soup.find_all("p")[status_int]
	final_status = str(job_elements).split(">")[3][:-10].strip()
	database_list.append(final_status)
	#print(url + "       ||||||||||         " + final_status) #### STILL NEEDS SOME FIXING TO DO
	###     COLLECTING CARTOON SUMMARY ###
	job_elements = soup.find_all("p")[summary_int]
	final_summary = str(job_elements).split(">")[1][:-3]
	#print(final_summary)
	database_list.append(final_summary)
	update_database(database_list)
	
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
    cur.execute("SELECT id,kim_url FROM Main_Cartoons")
    x=0
    rows = cur.fetchall()
    biggest = len(rows)
    for row in rows:
        id_nr = str(row[0]) 
        url = row[1]
        get_details(url,id_nr)
        x=x+1
        sys.stdout.write("\r" + "Updating cartoon details: "+ str(x) + "/" + str(biggest))

def main():
    database = r"Cartoon_db.sqlite"

    # create a database connection
    conn = create_connection(database)
    with conn:
        select_all_tasks(conn)
        sys.stdout.flush()


if __name__ == '__main__':
    main()
