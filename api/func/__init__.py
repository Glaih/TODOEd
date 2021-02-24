import logging
from pathlib import Path
from flask import Flask
from flask_migrate import Migrate

from config import BaseConfig
from func.database import db, User


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(BaseConfig())

    db.init_app(app)
    migrate = Migrate(app, db)

    logging.basicConfig(
        format='%(asctime)s - %(name)s:%(message)s',
        filename=Path(__file__, '../../app.log').resolve(),
        level=logging.DEBUG,
    )

    return app
