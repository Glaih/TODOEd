import sqlite3
import bcrypt
from flask import jsonify
import os.path
from func.validate import validation_response

path = str(os.path.abspath('./'))
db = path + '\\db\\auth.db'

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
    print(db)
    values = (email, password_hash(psw))
    user_get = validation_response(email, psw)
    if user_get is True:
        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()

            c.execute("INSERT INTO auth (mail, psw) VALUES (?, ?)", values)

            conn.commit()
            conn.close()

            return jsonify({'success': 'User has been registered'}), 200

        except sqlite3.IntegrityError:
            return jsonify({'duplicate_error': 'User already exists'}), 400
    else:
        return user_get
