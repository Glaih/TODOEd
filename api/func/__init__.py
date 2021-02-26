import logging
from pathlib import Path
from flask import Flask
from flask_migrate import Migrate

from func.blueprints import registration_blueprint
from config import BaseConfig, TestConfig
from func.database import db


def create_app(test_config=False):
    app = Flask(__name__)

    if test_config is True:
        app.config.from_object(TestConfig())
        print('test')
    else:
        app.config.from_object(BaseConfig())
        print('base')

    app.register_blueprint(registration_blueprint)

    db.init_app(app)
    migrate = Migrate(app, db)

    logging.basicConfig(
        format='%(asctime)s - %(name)s:%(message)s',
        filename=Path(__file__, '../../app.log').resolve(),
        level=logging.DEBUG,
    )

    return app
