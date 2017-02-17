from flask import Flask, render_template, request, jsonify

import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')


@app.route('/movie', methods = ['POST'])
def movie():
	connection = sqlite3.connect('database.db')
	cursor = connection.cursor()

	title = request.form['title']
	genre = request.form['genre']

	try:
		cursor.execute('INSERT INTO Movies(title, genre) VALUES (?, ?)', (title, genre))
		connection.commit()
		message = 'Succesfully inserted into Movies table'
	except:
		connection.rollback()
		message = 'There was an issue inserting data'
	finally:
		connection.close()
		return message


@app.route('/movies')
def movies():
	connection = sqlite3.connect('database.db')
	cursor = connection.cursor()
	cursor.execute('SELECT * from Movies')
	movies_list = cursor.fetchall()
	connection.close()
	return jsonify(movies_list)

app.run(debug = True)
