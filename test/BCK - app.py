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
		conn = sqlite3.connect('students.sqlite')
	except sqlite3.error as e:
		print(e)
	return conn

@app.route("/students" , methods=["GET","POST"])
def students():
	#access the db connection
	conn = db_connection()
	#access the cursor object
	cursor = conn.cursor()

#createing our GET request for all students
	if request.method == "GET":
		cursor = conn.execute("SELECT * FROM students")
		students = [
		  dict(id = row[0], firstname = row[1], lastname = row[2], gender = row[3] , age = row[4])
		  for row in cursor.fetchall()
		]

		if students is not None:
			return jsonify(students)
#createing our POST request for a student
	if request.method == "POST":
		firstname = request.form["firstname"]
		lastname = request.form["lastname"]
		gender = request.form["gender"]
		age  = request.form["age"]
		#SQL  query to INSERT a student INTO our database
		sql = """INSERT INTO students (firstname, lastname, gender, age)
				 VALUES (?, ?, ?, ?) """

		cursor = cursor.execute(sql, (firstname, lastname, gender, age))
		conn.commit()
		return f"Student with id: {cursor.lastrowid} created successfully"

#a route with all the neccesary request methods for a single student	
@app.route('/student/<int:id>',methods=[ "GET", "PUT", "DELETE" ])
def student(id):
	conn = db_connection()
	cursor = conn.cursor()
	student = None

#createing our GET request for a student
	if request.method == "GET":
		cursor.execute("SELECT * FROM students WHERE id=?",(id,) )
		rows = cursor.fetchall()
		for row in rows:
			student = row
		if student is not None:
			return jsonify(student), 200
		else:
			return "Something went wrong", 404

#createing our PUT request for a student
	if request.method == "PUT":
		sql = """ UPDATE students SET firstname = ?,lastname = ?, gender = ? , age = ?
				  WHERE id = ? """

		firstname = request.form["firstname"]
		lastname = request.form["lastname"]
		gender = request.form["gender"]
		age = request.form["age"]

		updated_student = {
			"id": id,
			"firstname": firstname,
			"lastname" : lastname,
			"gender" : gender,
			"age" : age
		}

		conn.execute(sql,(firstname, lastname, gender, age, id))
		conn.commit()
		return jsonify(updated_student)

#createing our DELETE request for a student
	if request.method == "DELETE":
		sql= """ DELETE FROM students WHERE id=? """
		conn.execute(sql, (id,))
		conn.commit()

		return "The Student with id: {} has been deleted.".format(id),200

if __name__ == '__main__':
    app.run(debug=True)
