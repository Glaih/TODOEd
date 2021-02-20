import logging
from flask import request

from func import create_app, User
from func.database import UserExistsError

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
            return User(mail=mail, password=password).create()
        except UserExistsError:
            logger.info(f"ERROR: 'User {mail} already exists.'")
            return {'errors': {'mail': 'User already exists'}}, 400
        finally:
            counter = 0
            errors_answer = {'errors': {}}
            errors_tuple = {'mail'}
            for e in User(mail=mail, password=password).create():
                if e == True


if __name__ == 'main':
    app.run()
