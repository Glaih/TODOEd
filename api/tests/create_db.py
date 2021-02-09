import sqlite3
from func.registration import DB_PATH
from pathlib import Path
import logging


logger = logging.getLogger(__name__)


def db_name(input_name):
    if '/' in list(input_name) or '\\' in list(input_name):
        input_name = ''.join([e for e in list(input_name) if e != '/' and e != '\\'])

    if input_name[-3:] == '.db':
        return input_name
    else:
        return input_name + '.db'


def create_base(name):
    conn = sqlite3.connect(Path(DB_PATH).parent / db_name(name))
    c = conn.cursor()

    try:
        c.execute('''CREATE TABLE auth (_id integer primary key autoincrement, mail text not null unique, psw text not null)''')
    except sqlite3.OperationalError:
        logger.exception("ERROR: 'Base already exist'")
        exit(1)

    conn.commit()
    conn.close()
    exit(0)


if __name__ == '__main__':
    create_base(str(input('Enter base name: ')))