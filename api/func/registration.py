import sqlite3
import bcrypt
import logging

from validate import validation_response


logger = logging.getLogger(__name__)

DB_PATH = 'db/test_auth.db'


# ------------------------------------------------------------------------------
# Creating hash for db from pw and checking if acquired pw matches hash from db.


def password_hash(psw):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(b'psw', salt)
    return hashed


def password_match(psw, hashed):
    if bcrypt.checkpw(psw, hashed):
        print("match")


# ------------------------------------------------------------------------------
# Writing usr mail and usr pw in user db.


def write_in_usr_db(email, psw):
    values = (email.strip(), password_hash(psw))
    user_get = validation_response(email.strip(), psw)
    if user_get is True:
        try:
            try:
                conn = sqlite3.connect(DB_PATH)
            except sqlite3.OperationalError:
                logger.exception("DB_ERROR: 'DB does not exist.'")
                quit()

            c = conn.cursor()

            c.execute("INSERT INTO auth (mail, psw) VALUES (?, ?)", values)

            conn.commit()
            conn.close()
            logger.info("SUCCESS: 'User has been registered.'")
            return {'success': 'User has been registered'}, 200

        except sqlite3.IntegrityError:
            logger.exception("ERROR: 'User already exists.'")
            return {'errors': {'mail': 'User already exists'}}, 400
    else:
        return user_get
