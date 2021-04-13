import re
import datetime
from bcrypt import hashpw, gensalt, checkpw
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    tasks = db.relationship('Task', backref='users', lazy=True)
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
        user = cls.get(email)

        if not user:
            raise PermissionErrors({'email': 'user does not exist'})
        if not checkpw(password.encode(), user.password.encode()):
            raise PermissionErrors({'password': 'incorrect password'})

        return user.id

    @classmethod
    def _validate(cls, email, password):
        errors = {}

        if cls.get(email):
            raise ValidationErrors({'email': 'User already exists'})

        if not cls.VALID_MAIL.search(email):
            errors['email'] = 'Invalid email'

        if not 8 <= len(password) <= 30:
            errors['password'] = 'Invalid password'

        if errors:
            raise ValidationErrors(errors)


class Task(db.Model):
    __tablename__ = 'tasks'
    task_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.String(180), nullable=False)
    deadline = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    @classmethod
    def create(cls, user_id, task_request):
        deadline = None
        title = task_request['title']
        text = task_request['text']
        if task_request['deadline']:
            deadline = task_request['deadline']
        task = cls(user_id=user_id, title=title, text=text, deadline=deadline)
        db.session.add(task)
        db.session.commit()
        return task.task_id


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
