import sqlite3
import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def clear_db(path):

    conn = sqlite3.connect(path)
    c = conn.cursor()

    c.execute('''DELETE FROM auth''')
    c.execute('''UPDATE sqlite_sequence SET seq = 0 WHERE name = "auth"''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    clear_db(str(input('Enter base name: ')))

