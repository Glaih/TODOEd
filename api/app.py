import logging
from flask import request

from func import create_app, User
from func.database import ValidationError
from config import TestConfig, BaseConfig

logger = logging.getLogger(__name__)


app = create_app()


@app.route('/api/v1/users/', methods=['POST'])
def registration():
    auth_request = request.get_json()
    try:
        mail = auth_request['email'].strip()
        password = auth_request['password']

    except TypeError as err:
        logger.exception(f"TYPE_ERROR: {err}")
        return {'type_error': f'{err}'}, 400

    except KeyError:
        logger.exception("JSON_KEY_ERROR: 'wrong keys'")
        return {'json_key_error': 'wrong keys'}, 400

    try:
        User(mail=mail, password=password).create()
        return {'success': 'User has been registered'}, 200
    except ValidationError as error:
        logger.exception(error)
        return error.get_errors(), 400


if __name__ == '__main__':
    app.run()
