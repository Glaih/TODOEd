import re
import logging
import bcrypt
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy


from app import app


logger = logging.getLogger(__name__)

DB_PATH = Path(__file__, '../../db/users.db').resolve()
DB_DIR = Path(DB_PATH).parent


if DB_PATH.is_file():
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    db = SQLAlchemy(app)
else:
    logger.debug("ERROR: 'Database doesn`t exist.'")
    quit(1)


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

                logger.info("SUCCESS: 'User has been registered.'")
                return {'success': 'User has been registered'}, 200

            logger.info(f"ERROR: 'User '{self.mail}' already exists.'")
            return {'errors': {'mail': 'User already exists'}}, 400

        return self._validation_response()

    def _validate_mail(self):
        return re.search(r"^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$", self.mail)

    def _validate_password(self):
        return 8 <= len(self.password) <= 30

    def _validation_response(self):
        if self._validate_mail() and self._validate_password():
            logger.info("SUCCESS: 'Mail and password are correct.'")
            return True

        elif not self._validate_mail() and self._validate_password():
            logger.info("ERROR: 'Incorrect email.'")
            return {'errors': {'email': 'Incorrect email'}}, 400

        elif not self._validate_password() and self._validate_mail():
            logger.info("ERROR: 'Password must be 8 - 30 symbols long.'")
            return {'errors': {'password': 'Password must be 8 - 30 symbols long'}}, 400

        elif not self._validate_mail() and not self._validate_password():
            logger.info("ERROR: 'password: Password must be 8 - 30 symbols long, email: Incorrect email.'")
            return {'errors': {'password': 'Password must be 8 - 30 symbols long',
                               'email': 'Incorrect email'}}, 400