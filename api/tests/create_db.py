from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DB_PASSWORD, DB_LOGIN, DB_HOST


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_LOGIN}:{DB_PASSWORD}@{DB_HOST}/test_users'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


if __name__ == '__main__':

    db.create_all()
