import logging
from pathlib import Path
from flask import Flask
from flask_migrate import Migrate

from core.blueprints import api_blueprint, jwt
from config import BaseConfig, TestConfig
from core.database import db


def create_app(test_config=False):
    app = Flask(__name__)

    config = TestConfig() if test_config else BaseConfig()
    app.config.from_object(config)

    app.register_blueprint(api_blueprint)

    jwt.init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    logging.basicConfig(
        format='%(asctime)s - %(name)s:%(message)s',
        filename=Path(__file__, '../../app.log').resolve(),
        level=logging.DEBUG,
    )

    return app
