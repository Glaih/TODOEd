import unittest
from unittest import mock
from pathlib import Path
from flask import url_for
import logging
import sqlite3
from bcrypt import checkpw

from app import app
from tests.clear_db import clear_db


logger = logging.getLogger(__name__)

TEST_DB_PATH = Path(__file__, '../../db/test_auth.db').resolve()


class TestBase(unittest.TestCase):
    @staticmethod
    def request(json_data):
        with app.test_request_context():
            response = app.test_client().post(url_for('registration'), json=json_data)
        data = response.get_json()

        return response, data


@mock.patch('func.registration.DB_PATH', TEST_DB_PATH)
class TestRegistration(TestBase):
    def setUp(self):
        clear_db(TEST_DB_PATH)

    @classmethod
    def tearDownClass(cls):
        clear_db(TEST_DB_PATH)

    def test_begin_valid(self):
        request_json = {"email": "tests@mail.ru", "password": "qwerty78"}
        response, data = self.request(request_json)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], "User has been registered")

    def test_double(self):
        request_json = {"email": "tests_doouble@mail.ru", "password": "qwerty789012345678901234567890"}
        self.request(request_json)
        response, data = self.request(request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'mail': 'User already exists'})

    def test_startswith_space_mail(self):
        request_json = {"email": " test3@mail.ru", "password": "qwerty789012345"}
        response, data = self.request(request_json)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], "User has been registered")

    def test_starts_endswith_space_mail(self):
        request_json = {"email": " test4@mail.ru ", "password": "qwerty432#%3fdDFG"}
        response, data = self.request(request_json)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], "User has been registered")

    def test_endswith_space_mail(self):
        request_json = {"email": "test5@mail.ru ", "password": "qwerty432#%3fdDFG"}
        response, data = self.request(request_json)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], "User has been registered")

    def test_short_password_no_tld(self):
        request_json = {"email": "test6@mail", "password": "qwerty7"}
        response, data = self.request(request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'password': 'Password must be 8 - 30 symbols long',
                                              'email': 'Incorrect email'})

    def test_no_at_mail(self):
        request_json = {"email": "test7mail.ru", "password": "qwerty432#%3fdDFG"}
        response, data = self.request(request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'email': 'Incorrect email'})

    def test_no_dot_mail(self):
        request_json = {"email": "test8@mail.com", "password": "1234567890123456789012345678901"}
        response, data = self.request(request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'password': 'Password must be 8 - 30 symbols long'})

    def test_password_length_zero(self):
        request_json = {"email": "test9@mail.com", "password": ""}
        response, data = self.request(request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'password': 'Password must be 8 - 30 symbols long'})

    def test_no_dot_no_at_mail(self):
        request_json = {"email": "test10mailcom", "password": "456789012345678901"}
        response, data = self.request(request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'email': 'Incorrect email'})

    def test_comma_instead_dot_mail(self):
        request_json = {"email": "test11@mail,com", "password": "112345678901"}
        response, data = self.request(request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'email': 'Incorrect email'})

    def test_comma_instead_at_mail(self):
        request_json = {"email": "test12,mail.com", "password": "456789012345678901"}
        response, data = self.request(request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'email': 'Incorrect email'})

    def test_not_json(self):
        request_json = 'not JSON'
        response, data = self.request(request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["type_error"], "data must be in json format")

    def test_wrong_keys(self):
        request_json = {"passworddd": "qwerty78"}
        response, data = self.request(request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["json_key_error"], "wrong keys")

    def test_password_written(self):
        password = 'Rgf6b33/Qd]'
        invalid_password = 'ctg45r[YFB!5'
        mail = ["test5@mail.ru"]

        self.request({"email": "test5@mail.ru ", "password": password})

        conn = sqlite3.connect(TEST_DB_PATH)
        c = conn.cursor()
        c.execute("SELECT psw FROM auth where mail=?", mail)
        password_in_db = c.fetchone()
        conn.commit()
        conn.close()

        self.assertTrue(checkpw(password.encode(), *password_in_db))
        self.assertFalse(checkpw(invalid_password.encode(), *password_in_db))


if __name__ == '__main__':
    app.run(debug=True)