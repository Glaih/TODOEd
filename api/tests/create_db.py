import sqlite3
import logging
from pathlib import Path

from func.registration import DB_DIR


logger = logging.getLogger(__name__)


def clear_db_name(input_name):
    input_name = input_name.replace('/', '')
    input_name = input_name.replace('\\', '')

    if input_name.endswith('.db'):
        return input_name
    else:
        return f'{input_name}.db'


def create_base(name):
    path = DB_DIR / clear_db_name(name)

    if path.is_file():
        logger.error("ERROR: 'Database already exist'")
        return {'errors': {'database': 'Database already exist'}}, 400

    conn = sqlite3.connect(path)
    c = conn.cursor()

    c.execute('''CREATE TABLE auth (_id integer primary key autoincrement, 
                                    mail text not null unique, psw text not null)''')

    conn.commit()
    conn.close()
    exit(0)


if __name__ == '__main__':
    create_base(str(input('Enter base name: ')))
