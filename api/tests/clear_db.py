import sqlite3
import logging


logger = logging.getLogger(__name__)


def clear_db(path):
    try:
        conn = sqlite3.connect(path)
    except sqlite3.OperationalError:
        logger.exception(f'DB_ERROR: DB {path=} does not exist.')
        quit()

    c = conn.cursor()

    c.execute('''DELETE FROM auth''')
    c.execute('''UPDATE sqlite_sequence SET seq = 0 WHERE name = "auth"''')

    conn.commit()
    conn.close()

