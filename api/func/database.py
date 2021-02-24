import re
import bcrypt
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def create(self):
        self._validate()
        password_hashed = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())
        db.session.add(User(mail=self.mail, password=password_hashed))
        db.session.commit()

    def _validate_mail(self):
        return bool(re.search(r"^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$", self.mail))

    def _validate_password(self):
        return bool(8 <= len(self.password) <= 30)

    def _validate(self):
        errors = {}

        if User.query.filter_by(mail=self.mail).first():
            errors['email'] = 'User already exists'

        if not self._validate_mail():
            errors['email'] = 'Invalid email'

        if not self._validate_password():
            errors['password'] = 'Invalid password'

        if errors:
            raise ValidationError(errors)


class UserExistsError(Exception):
    pass


class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors

    def get_errors(self):
        return {'errors': self.errors}

