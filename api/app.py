import logging
from flask import request

from func import create_app, User
from func.database import ValidationError

logger = logging.getLogger(__name__)

app = create_app()


@app.route('/api/v1/users/', methods=['POST'])
def registration():
    try:
        mail = request.get_json()['email']
        password = request.get_json()['password']

    except TypeError as err:
        logger.exception(f"TYPE_ERROR: {err}")
        return {'type_error': f'{err}'}, 400

    except KeyError:
        logger.exception("JSON_KEY_ERROR: 'wrong keys'")
        return {'json_key_error': 'wrong keys'}, 400

    else:
        try:
            User(mail=mail, password=password).create()
            return {'success': 'User has been registered'}, 200
        except ValidationError as error:
            logger.exception(error)
            return error.return_error(), 400


if __name__ == 'main':
    app.run()
