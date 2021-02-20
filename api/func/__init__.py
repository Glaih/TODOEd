import logging
from pathlib import Path
from flask import Flask

from config import BaseConfig
from func.database import db, User


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(BaseConfig())
    db.init_app(app)

    logging.basicConfig(
        format='%(asctime)s - %(name)s:%(message)s',
        filename=Path(__file__, '../../app.log').resolve(),
        level=logging.DEBUG,
    )

    return app
