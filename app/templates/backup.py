from flask import * # render_template, flash, redirect, request
from functools import wraps
import sqlite3
import hashlib

DATABASE = 'testdb.db'

app = Flask(__name__)
app.config.from_object(__name__)
# app.config["APPLICATION_ROOT"] = "/user"

app.secret_key = '4fsdfsfq'


def connect_db():
	return sqlite3.connect(app.config['DATABASE'])



def login_required(x):
	@wraps(x)
	def wrap(*args, **kwargs):
		if 'loggedin' in session:
			return x(*args, **kwargs)
		else:
			flash('You need to login.')
			return redirect('/user/login')
	return wrap



def generate_knockseq(name):
	m = hashlib.md5()
	m.update(name)
	hexValue = m.hexdigest()
	seqChar = ""
	for i in range (0,4):
		a = int(hexValue[i],16) % 4 
		seqChar = seqChar + str(a)
	#This will produce the knock sequence for the given usernam
	return seqChar



#@app.route('/')
#@app.route('/index')
#def index():
	# return "Hello, World!"
	#return render_template('index.html')



@app.route('/')
def index():
	return redirect('/user/login')



@app.route('/user/register', methods=['GET', 'POST'])
def register():
	username = None
	password = None
	seq = None
	error = None

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		confirm_pswd = request.form['password_confirm']

		if len(username) == 0 or len(password) == 0:
			error = 'Please enter all the details.'
		elif password != confirm_pswd:
			error = 'Password does not match.'
		else:
			conn = connect_db()
			cur = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
			result = cur.fetchone()

			if result is None:
				kseq = int(generate_knockseq(username))
				cur = conn.cursor()
				cur.execute("INSERT INTO users(username, password, sequence) VALUES (?,?,?)", (username, password, kseq))
				conn.commit()
				conn.close()
				return redirect('/user/login')
			else:
				conn.close()
				error = 'Username already exist. Try different username.'

	return render_template('register.html', error = error)



@app.route('/user/login', methods=['GET', 'POST'])
def login():
	#session.pop('loggedin', None)
	error = None
	username = None
	password = None
	logged = None

	try:
		if session['loggedin']:
			print 'Session: ' + str(session['loggedin'])
			logged = True
	except KeyError:
		print "Keyerror"
		logged = False

		
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		
		conn = connect_db()
		cur = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
		result = cur.fetchone()
		conn.close()

		if len(username) == 0 or len(password) == 0:
			error = 'Please enter all the details.'
		elif result is None:
			error = 'Username not found.'
		elif password != result[2]:
			error = 'Invalid credentials. Please try again.'
		else:
			session['loggedin'] = True
			print "setting it true"
		#	session['user_id'] = result[0]
			return redirect('/message/add')
	return render_template('login.html', error = error, logged = logged)



@app.route('/user/logout')
def logout():
	session.pop('user_id', None)
	# session.pop('loggedin', None)
	session['loggedin'] = False
	flash('You are logged out.')
	return redirect('/user/login')



@app.route('/message/list')
@login_required
def list():
	#conn = connect_db()
	#cur = conn.execute('select * from messages')
	#messages = [dict(message = row[0])] for row in cur.fetchall()]
	#conn.close()
	return render_template('list_msg.html')



@app.route('/message/add')
@login_required
def add():
	#conn = connect_db()
	#cur = conn.execute('select message from messages')
	#messages = [dict(message = row[0])] for row in cur.fetchall()]
	#conn.close()
	return render_template('add_msg.html')



#@app.route('/blog', methods=['GET', 'POST'])
#@login_required
#def blog():
	#conn = connect_db()
	#cur = conn.execute('select message from messages')
	#messages = [dict(message = row[0])] for row in cur.fetchall()]
	#conn.close()
	#name = None
	#message = None
	#if request.method == 'POST' and 'name' in request.form and 'message' in request.form:
		#name = request.form['name']
		#message = request.form['message']
	#return render_template('blog.html', title = 'Blog', 
		#		name = name, message = message)


if __name__ == '__main__':
	app.run(debug=True)

