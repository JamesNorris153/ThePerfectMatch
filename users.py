import sqlite3 as sql
from os import path

ROOT = path.dirname(path.relpath((__file__)))

#Example Methods
def create_user(applicant):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT INTO users (email,name) VALUES (?,?)',(applicant.email,applicant.first_name))
    con.commit()
    con.close()

def get_users():
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    con.close()
    return users

def get_user(id):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM users WHERE id=?',(id))
    user = cur.fetchall()
    con.close()
    return user

def authenticate_user(email, password):
	# not implemented yet
	return False
