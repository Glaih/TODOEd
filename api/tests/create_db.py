import sqlite3
from func.registration import DB_PATH

conn = sqlite3.connect('../' + DB_PATH)

c = conn.cursor()

c.execute('''CREATE TABLE auth (_id integer primary key autoincrement, mail text not null unique, psw text not null)''')

conn.commit()
conn.close()
