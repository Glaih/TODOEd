from flask import Flask


app = Flask(__name__)


@app.route('/api/v1/users/')
def ok():
    return 'OK', 200


if __name__ == '__main__':
    app.run()
