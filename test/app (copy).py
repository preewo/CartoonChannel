from flask import Flask, request,jsonify, render_template
import  json
import sqlite3

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

@app.route("/cartoons" , methods=["GET","POST"])
def cartoons():
	#access the db connection
	conn = db_connection()
	#access the cursor object
	cursor = conn.cursor()

#createing our GET request for all students
	if request.method == "GET":
		cursor = conn.execute("SELECT * FROM Main_Cartoons")
		cartoons = [
		  dict(id = row[0], main_title = row[1], kim_url = row[2])
		  for row in cursor.fetchall()
		]
		if cartoons is not None:
			return jsonify(cartoons)

#a route with all the neccesary request methods for a single student	
@app.route('/cartoons/<int:id>',methods=[ "GET", "PUT", "DELETE" ])
def cartoon(id):
	conn = db_connection()
	cursor = conn.cursor()
	cartoon = None

#createing our GET request for a student
	if request.method == "GET":
		cursor.execute("SELECT * FROM Main_Cartoons WHERE id=?",(id,) )
		rows = cursor.fetchall()
		for row in rows:
			cartoon = row
		if cartoon is not None:
			return jsonify(cartoon), 200
		else:
			return "Something went wrong", 404

#createing our PUT request for a student

if __name__ == '__main__':
    app.run(debug=True)
