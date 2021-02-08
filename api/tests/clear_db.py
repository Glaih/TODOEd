import sqlite3


def clear_db(path):
    conn = sqlite3.connect(path)

    c = conn.cursor()

    c.execute('''DELETE FROM auth''')
    c.execute('''UPDATE sqlite_sequence SET seq = 0 WHERE name = "auth"''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    clear_db('../db/auth.db')
