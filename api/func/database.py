import re
import bcrypt
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def create(self):
        self._validation_response()
        password_hashed = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())
        db.session.add(User(mail=self.mail, password=password_hashed))
        db.session.commit()

    def _validate_mail(self):
        return bool(re.search(r"^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$", self.mail))

    def _validate_password(self):
        return bool(8 <= len(self.password) <= 30)

    def _validation_response(self):
        errors = {}

        if User.query.filter_by(mail=self.mail).first() is not None:
            errors['email'] = 'User already exists'

        if self._validate_mail() is False:
            errors['email'] = 'Invalid email'

        if self._validate_password() is False:
            errors['password'] = 'Invalid password'

        if errors:
            raise ValidationError(errors)


class UserExistsError(Exception):
    pass


class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors

    def return_error(self):
        return {'Errors': self.errors}

