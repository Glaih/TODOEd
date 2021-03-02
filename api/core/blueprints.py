import logging
from flask import request, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity

from core.database import ValidationError, User


logger = logging.getLogger(__name__)


api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/api/v1/users/', methods=['POST'])
def registration():
    auth_request = request.get_json()

    if not check_errors(auth_request)[0]:
        mail, password = check_errors(auth_request)[1:3]

        try:
            User.create(email=mail, password=password)
            return {'success': 'User has been registered'}, 200
        except ValidationError as error:
            logger.exception(error)
            return error.get_errors(), 400

    else:
        return check_errors(auth_request)


@api_blueprint.route('/api/v1/users/login', methods=['POST'])
def login():
    auth_request = request.get_json()

    if not check_errors(auth_request)[0]:
        mail, password = check_errors(auth_request)[1:3]

        if mail != "test@mail.ru" or password != "test":
            return {"msg": "Bad username or password"}, 401

        access_token = create_access_token(identity=mail)
        refresh_token = create_refresh_token(identity=mail)
        return {'access_token': access_token, 'refresh_token': refresh_token}, 200

    else:
        return check_errors(auth_request)


@api_blueprint.route('/api/v1/users/refresh', methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {'access_token': access_token}, 200


@api_blueprint.route('/api/v1/users/jwt_Protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return {'logged_in_as': current_user}, 200


def check_errors(json):
    try:
        mail = json['email']
        password = json['password']
        return False, mail, password

    except TypeError as err:
        logger.exception(f"TYPE_ERROR: {err}")
        return {'type_error': f'{err}'}, 400

    except KeyError:
        logger.exception("JSON_KEY_ERROR: 'wrong keys'")
        return {'json_key_error': 'wrong keys'}, 400
