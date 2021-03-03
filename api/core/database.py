import re
from bcrypt import hashpw, gensalt, checkpw
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    @classmethod
    def create(cls, email, password):
        email = email.strip()
        hashed_password = hashpw(password.encode(), gensalt())
        user = cls(mail=email, password=hashed_password)
        return user.save(email, password)

    def save(self, email, raw_password):
        self._validate(email, raw_password)
        if self._id is None:
            db.session.add(self)
        else:
            pass  # TODO add code for changing user email/password.

        db.session.commit()
        return self

    @classmethod
    def verify_user(cls, email, password):
        email = email.strip()
        user = cls.query.filter_by(mail=email).first()
        cls._verificate_user(email, password, user)
        return True

    @staticmethod
    def _verificate_user(email, password, user_object):
        errors = {}

        if not User.query.filter_by(mail=email).first():
            errors['mail'] = 'user does not exist'

        else:
            if not checkpw(password.encode(), user_object.password):
                errors['password'] = 'incorrect password'  # TODO Implement some CAPTCHAlike verification.

        if errors:
            raise VerificationError(errors)

    @staticmethod
    def _validate_mail(mail):
        return bool(re.search(r"^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$", mail))

    @staticmethod
    def _validate_password(password):
        return bool(8 <= len(password) <= 30)

    def _validate(self, email, password):
        errors = {}

        if User.query.filter_by(mail=email).first():
            errors['email'] = 'User already exists'

        if not self._validate_mail(email):
            errors['email'] = 'Invalid email'

        if not self._validate_password(password):
            errors['password'] = 'Invalid password'

        if errors:
            raise ValidationError(errors)


class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors

    def get_errors(self):
        return {'errors': self.errors}


class VerificationError(Exception):
    def __init__(self, errors):
        self.errors = errors

    def get_errors(self):
        return {'errors': self.errors}
