import sqlite3

conn = sqlite3.connect('db/auth.db')

c = conn.cursor()

c.execute('''DELETE FROM auth ''')
c.execute('''UPDATE sqlite_sequence SET seq = 0 WHERE name = "auth"''')

conn.commit()
conn.close()
