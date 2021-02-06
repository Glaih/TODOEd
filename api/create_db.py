import sqlite3

conn = sqlite3.connect('db/auth.db')

c = conn.cursor()

c.execute('''CREATE TABLE auth (_id integer primary key autoincrement, mail text not null, psw text not null)''')

conn.commit()
conn.close()
