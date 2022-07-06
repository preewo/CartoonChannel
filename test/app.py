from flask import Flask, render_template, request, url_for, flash, redirect
import json
import sqlite3
import datetime

app = Flask(__name__)

#an in memory students storage(using a list)
#students = []
#instead of a list,we need to create a connection to database where we store students
def db_connection():
	conn = None
	try:
		conn = sqlite3.connect('Cartoon_db.db')
	except sqlite3.error as e:
		print(e)
	return conn

@app.route('/')
def index():
	conn = db_connection()
	cursor = conn.execute("SELECT * FROM Main_Cartoons LIMIT 10")
	posts = cursor.fetchall()
	return render_template('index.html', posts=posts)
	
if __name__ == '__main__':
    app.run(debug=True)
