import sqlite3
from app_logger import app_logger


logger = app_logger(__name__)


def clear_db(path):
    try:
        conn = sqlite3.connect(path)
    except sqlite3.OperationalError:
        logger.exception('DB_ERROR: DB does not exist.')
        quit()

    c = conn.cursor()

    c.execute('''DELETE FROM auth''')
    c.execute('''UPDATE sqlite_sequence SET seq = 0 WHERE name = "auth"''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    clear_db('../db/auth.db')
