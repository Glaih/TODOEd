import re
from sqlalchemy import exc
from datetime import datetime, timezone
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
    def get(cls, email=None, user_id=None, status=None):
        if email:
            user = cls.query.filter_by(mail=email).first()
        elif user_id:
            user = cls.query.filter_by(id=user_id).first()
        elif status:
            user = cls.query.filter_by(is_active=status).first()

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
    deadline = db.Column(db.DateTime(timezone=True), default=None)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now(tz=timezone.utc))

    @classmethod
    def create(cls, user_id, title, text, deadline):
        title = title.strip()
        text = text.strip()

        task = cls(user_id=user_id, title=title, text=text, deadline=deadline)

        return task.save(title, text, deadline, user_id)

    def save(self, title, text, deadline, user_id):
        self._validate(title, text, deadline)
        if self.task_id is None:
            db.session.add(self)
        else:
            pass

        try:
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()

            if f'(user_id)=({user_id}) is not present in table "users"' in str(e.orig):
                raise ValidationErrors({"user_id": f"{user_id=} doesn't exists"})
            raise ValidationErrors(str(e.orig))

        return self

    @classmethod
    def get_one(cls, task_id):
        task = cls.query.filter_by(task_id=task_id).first()
        return task

    @classmethod
    def _validate(cls, title, text, deadline):
        errors = {}

        if not 1 <= len(title) <= 30:
            errors['title'] = 'Title must be 1-30 chars long'

        if not 1 <= len(text) <= 180:
            errors['text'] = 'Text must be 1-180 chars long'

        if deadline:
            try:
                datetime.fromisoformat(deadline)
                if datetime.now(tz=timezone.utc) >= datetime.fromisoformat(deadline):
                    errors['deadline'] = 'Deadline cannot be from past'
            except ValueError as e:
                errors['deadline'] = str(e)
            except TypeError as e:
                errors['deadline'] = 'Deadline must have timezone'

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
