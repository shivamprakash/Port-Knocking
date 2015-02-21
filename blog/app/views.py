from flask import * # render_template, flash, redirect, request
from functools import wraps
import sqlite3
import hashlib

DATABASE = 'testdb.db'

app = Flask(__name__)
app.config.from_object(__name__)
# app.config["APPLICATION_ROOT"] = "/user"

app.secret_key = '4fsdfsfq'

#@app.before_request
#def func():
	#session.clear()

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
	#This will produce the knock sequence for the given username
	return seqChar



def set_kseq():
	session['kseq'] = ''



def append_keq(x):
	try:
		if session['username']:
			if len(session['kseq']) == 4:
				temp = session['kseq']
				session['kseq'] = temp[1:]

			session['kseq'] += x

			if len(session['kseq']) == 4 and session['okseq'] == int(session['kseq']):
				session['secret'] = 1
				#print str(session['secret'])
				
			print "length " + str(session['kseq'])
	except KeyError:
		print "KeyError"



@app.route('/')
def index():
	return redirect('/user/login')



@app.route('/user/register', methods=['GET', 'POST'])
def register():
	username = None
	password = None
	seq = None
	error = None

	append_keq('0')

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
				kseq = generate_knockseq(username)
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
	error = None
	username = None
	password = None
	logged = None

	append_keq('1')

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
			session['user_id'] = result[0]
			session['username'] = result[1]
			session['okseq'] = int(result[3])
			session['secret'] = 0
			set_kseq()
	return render_template('login.html', error = error)



@app.route('/user/logout')
def logout():
	session.clear()
	print "Clear session"
	flash('You are logged out.')
	return redirect('/user/login')



@app.route('/message/list')
@login_required
def list():
	append_keq('3')	
	try:
		conn = connect_db()
		cur = conn.execute('''Select * from messages WHERE is_secret=? ''',(session['secret'],))
		all_rows = cur.fetchall()
	except KeyError:
		print "KeyError"
	conn.close()

	return render_template('list_msg.html',
	                       messages=all_rows)



@app.route('/message/add', methods=['GET', 'POST'])
@login_required
def add():
	append_keq('2')

	title = None
	message = None
	error = None
	success = None

	if request.method == 'POST':
		title = request.form['title']
		message = request.form['message']

		if len(title) == 0 or len(message) == 0:
			error = 'Please enter Title and Message.'
		else:
			conn = connect_db()
			cur = conn.cursor()
			cur.execute("INSERT INTO messages(title, message, userid, username, is_secret) VALUES (?,?,?,?,?)", (title, message, session['user_id'], session['username'], session['secret']))
			conn.commit()
			conn.close()
			success = True
	return render_template('add_msg.html', error = error, title = title, success = success)



@app.before_first_request
def _run_on_start():
	session.clear()



if __name__ == '__main__':
	app.run(debug=True)

