from flask import Flask, request, jsonify
from func.registration import write_in_usr_db


app = Flask(__name__)


@app.route('/api/v1/users/', methods=['POST'])
def registration():
    try:
        auth_request = request.get_json()

        return write_in_usr_db(auth_request['email'], auth_request['password'])

    except TypeError:
        return jsonify({'type_error': 'data must be in json format'}), 400
    except KeyError:
        return jsonify({'json_key_error': 'wrong keys'}), 400


if __name__ == '__main__':
    app.run(debug=True)
