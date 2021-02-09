import sqlite3
from func.registration import DB_DIR
from pathlib import Path
import logging


logger = logging.getLogger(__name__)


def clear_db_name(input_name):
    input_name = input_name.replace('/', '')
    input_name = input_name.replace('\\', '')

    if input_name.endswith('.db'):
        return input_name
    else:
        return f'{input_name}.db'


def create_base(name):
    conn = sqlite3.connect(DB_DIR / clear_db_name(name))
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