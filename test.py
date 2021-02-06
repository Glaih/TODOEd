import sqlite3

conn = sqlite3.connect('auth.db')

c = conn.cursor()

c.execute('''CREATE TABLE auth (_id integer primary key autoincrement , mail text, psw text)''')

conn.commit()
conn.close()
