import psycopg2
from contextlib import closing
from config import DB_PASSWORD, DB_LOGIN, DB_HOST


def clear_db(db):
    with closing(psycopg2.connect(dbname=db, user=DB_LOGIN,
                                  password=DB_PASSWORD, host=DB_HOST)) as conn:
        with conn.cursor() as cursor:
            cursor.execute("TRUNCATE users")
            cursor.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1")
            conn.commit()


if __name__ == '__main__':
    clear_db('users')
