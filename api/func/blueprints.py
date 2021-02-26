import logging
from flask import request, Blueprint

from func.database import ValidationError, User


logger = logging.getLogger(__name__)

registration_blueprint = Blueprint('registration', __name__)


@registration_blueprint.route('/api/v1/users/', methods=['POST'])
def registration():
    auth_request = request.get_json()
    try:
        mail = auth_request['email']
        password = auth_request['password']

    except TypeError as err:
        logger.exception(f"TYPE_ERROR: {err}")
        return {'type_error': f'{err}'}, 400

    except KeyError:
        logger.exception("JSON_KEY_ERROR: 'wrong keys'")
        return {'json_key_error': 'wrong keys'}, 400

    try:
        User.create(email=mail, password=password)
        return {'success': 'User has been registered'}, 200
    except ValidationError as error:
        logger.exception(error)
        return error.get_errors(), 400
