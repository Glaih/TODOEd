import re
import logging
import bcrypt
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__, '../../db/users.db').resolve()
DB_DIR = Path(DB_PATH).parent


db = SQLAlchemy()


class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def create(self):
        if self._validation_response() is True:
            password_hashed = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())
            if User.query.filter_by(mail=self.mail).first() is None:
                db.session.add(User(mail=self.mail, password=password_hashed))
                db.session.commit()

                return {'success': 'User has been registered'}, 200

            raise UserExistsError

        return self._validation_response()

    def _validate_mail(self):
        return bool(re.search(r"^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$", self.mail))

    def _validate_password(self):
        return bool(8 <= len(self.password) <= 30)

    def _validation_response(self):
        if self._validate_mail() and self._validate_password():
            return True

        else:
            return self._validate_mail(), self._validate_password()


class UserExistsError(Exception):
    pass



