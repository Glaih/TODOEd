import re
from bcrypt import hashpw, gensalt, checkpw
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    VALID_MAIL = re.compile(r"^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$")

    @classmethod
    def create(cls, email, password):
        email = email.strip()
        hashed_password = hashpw(password.encode(), gensalt())
        user = cls(mail=email, password=hashed_password.decode())
        return user.save(email, password)

    def save(self, email, raw_password):
        self._validate(email, raw_password)
        if self.id is None:
            db.session.add(self)
        else:
            pass

        db.session.commit()
        return self

    @classmethod
    def get(cls, email):
        user = cls.query.filter_by(mail=email).first()
        return user

    @classmethod
    def verify(cls, email, password):
        email = email.strip()
        user = cls.query.filter_by(mail=email).first()

        if not user:
            raise PermissionErrors({'email': 'user does not exist'})
        if not checkpw(password.encode(), user.password.encode()):
            raise PermissionErrors({'password': 'incorrect password'})

        return user.id

    def _validate(self, email, password):
        errors = {}

        if User.query.filter_by(mail=email).first():
            raise ValidationErrors({'email': 'User already exists'})

        if not self.VALID_MAIL.search(email):
            errors['email'] = 'Invalid email'

        if not 8 <= len(password) <= 30:
            errors['password'] = 'Invalid password'

        if errors:
            raise ValidationErrors(errors)


class BaseErrors(Exception):
    status_code = 400

    def __init__(self, errors):
        self.errors = errors

    def get_errors(self):
        return {'errors': self.errors}


class ValidationErrors(BaseErrors):
    pass


class PermissionErrors(BaseErrors):
    status_code = 403


if __name__ == '__main__':
    db.create_all()
