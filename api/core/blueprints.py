import logging
from flask import request, Blueprint, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity

from core.database import ValidationError, User


logger = logging.getLogger(__name__)
jwt = JWTManager()

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/api/v1/users/', methods=['POST'])
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


@api_blueprint.route('/api/v1/users/login', methods=['POST'])
def login():
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

    if mail != "test" or password != "test":
        return {"msg": "Bad username or password"}, 401

    access_token = create_access_token(identity=mail)
    refresh_token = create_refresh_token(identity=mail)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@api_blueprint.route('/api/v1/users/refresh', methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@api_blueprint.route('/api/v1/users/JWT_Protected', methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

