from flask import Flask, request
from func.registration import write_in_usr_db


app = Flask(__name__)


@app.route('/api/v1/users/', methods=['POST', 'GET'])
def ok():
    auth_request = request.get_json()

    return write_in_usr_db(auth_request['email'], auth_request['password'])


if __name__ == '__main__':
    app.run(debug=True)
