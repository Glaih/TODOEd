import sqlite3
import bcrypt
import logging
from pathlib import Path

from .validate import validation_response


logger = logging.getLogger(__name__)

DB_PATH = Path(__file__, '../../db/auth.db').resolve()
DB_DIR = Path(DB_PATH).parent

# ------------------------------------------------------------------------------
# Creating hash for db from pw and checking if acquired pw matches hash from db.


def password_hash(psw):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(psw.encode(), salt)
    return hashed


def password_match(psw, hashed):
    return bcrypt.checkpw(psw, hashed)


# ------------------------------------------------------------------------------
# Writing usr mail and usr pw in user db.


def write_in_usr_db(email, psw):
    values = (email.strip(), password_hash(psw))
    user_get = validation_response(email.strip(), psw)
    if user_get is True:
        try:
            conn = sqlite3.connect(DB_PATH)
        except sqlite3.OperationalError:
            logger.exception(f"DB_ERROR: 'DB {DB_PATH=} does not exist.'")
            quit()

        c = conn.cursor()

        try:
            c.execute("INSERT INTO auth (mail, psw) VALUES (?, ?)", values)
        except sqlite3.IntegrityError:
            logger.exception("ERROR: 'User already exists.'")
            return {'errors': {'mail': 'User already exists'}}, 400

        conn.commit()
        conn.close()
        logger.info("SUCCESS: 'User has been registered.'")
        return {'success': 'User has been registered'}, 200

    return user_get
