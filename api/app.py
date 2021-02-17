from flask import Flask, request
import logging
from pathlib import Path

from func.database import User

logging.basicConfig(
    format='%(asctime)s - %(name)s:%(message)s',
    filename=Path(__file__, '../app.log').resolve(),
    level=logging.DEBUG,
)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logger = logging.getLogger(__name__)


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
        return User(mail=mail, password=password).create()


if __name__ == '__main__':
    app.run(debug=True)
