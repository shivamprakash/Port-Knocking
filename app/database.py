import sqlite3 as lite
import sys

admin_users = (
	('admin1', 'admin1')
)

conn = lite.connect('testdb.db')

with conn:
	cur = conn.cursor()

	cur.execute("DROP TABLE IF EXISTS users")
	cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, sequence TEXT)")
	# cur.execute("INSERT INTO users (username, password) VALUES(?, ?)", admin_users)

	cur.execute("DROP TABLE IF EXISTS messages")
	cur.execute("CREATE TABLE messages(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, message TEXT, userid INTEGER, username TEXT, is_secret NUMERIC)")
