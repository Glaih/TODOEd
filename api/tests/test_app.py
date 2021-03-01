import unittest
import logging
import sqlite3
from flask import url_for
from bcrypt import checkpw

from core import create_app
from tests.clear_db import clear_db
from config import TEST_DB_PATH

logger = logging.getLogger(__name__)

app = create_app(True)


class TestBase(unittest.TestCase):
    @staticmethod
    def request(json_data, endpoint, method='post'):
        if method == 'post':
            with app.test_request_context():
                response = app.test_client().post(url_for(endpoint), json=json_data)
            data = response.get_json()
        else:
            with app.test_request_context():
                response = app.test_client().get(url_for(endpoint), json=json_data)
            data = response.get_json()

        return response, data


class TestRegistrationErrors(TestBase):
    def setUp(self):
        self.endpoint = 'api.registration'

    def test_short_password_no_tld(self):
        request_json = {"email": "test6@mail", "password": "qwerty7"}
        response, data = self.request(request_json, self.endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'password': 'Invalid password', 'email': 'Invalid email'}, data["errors"])

    def test_no_at_mail(self):
        request_json = {"email": "test7mail.ru", "password": "qwerty432#%3fdDFG"}
        response, data = self.request(request_json, self.endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'email': 'Invalid email'}, data["errors"])

    def test_no_dot_mail(self):
        request_json = {"email": "test8@mail.com", "password": "1234567890123456789012345678901"}
        response, data = self.request(request_json, self.endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'password': 'Invalid password'}, data["errors"])

    def test_password_length_zero(self):
        request_json = {"email": "test9@mail.com", "password": ""}
        response, data = self.request(request_json, self.endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'password': 'Invalid password'}, data["errors"])

    def test_no_dot_no_at_mail(self):
        request_json = {"email": "test10mailcom", "password": "456789012345678901"}
        response, data = self.request(request_json, self.endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'email': 'Invalid email'}, data["errors"])

    def test_comma_instead_dot_mail(self):
        request_json = {"email": "test11@mail,com", "password": "112345678901"}
        response, data = self.request(request_json, self.endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'email': 'Invalid email'}, data["errors"])

    def test_comma_instead_at_mail(self):
        request_json = {"email": "test12,mail.com", "password": "456789012345678901"}
        response, data = self.request(request_json, self.endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'email': 'Invalid email'}, data["errors"])

    def test_type_error(self):
        request_json = 21
        response, data = self.request(request_json, self.endpoint)

        self.assertEqual(400, response.status_code)
        self.assertTrue('type_error' in data)

    def test_wrong_keys(self):
        request_json = {"passworddd": "qwerty78"}
        response, data = self.request(request_json, self.endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual("wrong keys", data["json_key_error"])


@unittest.skipIf(TEST_DB_PATH.is_file() == 0, f'DB_ERROR: DB does not exist.')
class TestRegistrationDb(TestBase):

    def setUp(self):
        clear_db(TEST_DB_PATH)
        self.endpoint = 'api.registration'

    @classmethod
    def tearDownClass(cls):
        clear_db(TEST_DB_PATH)

    def test_begin_valid(self):
        request_json = {"email": "tests@mail.ru", "password": "qwerty78"}
        response, data = self.request(request_json, self.endpoint)

        self.assertEqual(200, response.status_code)
        self.assertEqual("User has been registered", data["success"])

    def test_double(self):
        request_json = {"email": "tests_doouble@mail.ru", "password": "qwerty789012345678901234567890"}
        self.request(request_json, self.endpoint)
        response, data = self.request(request_json, self.endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'email': 'User already exists'}, data["errors"])

    def test_startswith_space_mail(self):
        request_json = {"email": " test3@mail.ru", "password": "qwerty789012345"}
        response, data = self.request(request_json, self.endpoint)

        self.assertEqual(200, response.status_code)
        self.assertEqual("User has been registered", data["success"])

    def test_starts_endswith_space_mail(self):
        request_json = {"email": " test4@mail.ru ", "password": "qwerty432#%3fdDFG"}
        response, data = self.request(request_json, self.endpoint)

        self.assertEqual(200, response.status_code)
        self.assertEqual("User has been registered", data["success"])

    def test_endswith_space_mail(self):
        request_json = {"email": "test5@mail.ru ", "password": "qwerty432#%3fdDFG"}
        response, data = self.request(request_json, self.endpoint)

        self.assertEqual(200, response.status_code)
        self.assertEqual("User has been registered", data["success"])

    def test_password_written(self):
        password = 'Rgf6b33/Qd]'
        invalid_password = 'ctg45r[YFB!5'
        mail = ["test5@mail.ru"]

        self.request({"email": "test5@mail.ru ", "password": password}, self.endpoint)

        conn = sqlite3.connect(TEST_DB_PATH)
        c = conn.cursor()
        c.execute("SELECT password FROM user where mail=?", mail)

        password_in_db = c.fetchone()

        conn.commit()
        conn.close()

        self.assertTrue(checkpw(password.encode(), *password_in_db))
        self.assertFalse(checkpw(invalid_password.encode(), *password_in_db))


class TestJWT(TestBase):
    @classmethod
    def setUpClass(cls):
        cls.login = 'api.login'
        cls.refresh = 'api.refresh'
        cls.protected = 'api.protected'

    def test_login_type_error(self):
        request_json = 21
        response, data = self.request(request_json, self.login)

        self.assertEqual(400, response.status_code)
        self.assertTrue('type_error' in data)

    def test_login_wrong_keys(self):
        request_json = {"passworddd": "qwerty78"}
        response, data = self.request(request_json, self.login)

        self.assertEqual(400, response.status_code)
        self.assertEqual("wrong keys", data["json_key_error"])

    def test_acquire_jwt(self):
        request_json = {"email": "test@mail.ru", "password": "test"}

        response, data = self.request(request_json, self.login)

        self.assertEqual(200, response.status_code)
        self.assertEqual(['access_token', 'refresh_token'], list(data.keys()))

    def test_refresh_jwt(self):
        request_jwt = {"email": "test@mail.ru", "password": "test"}

        data = self.request(request_jwt, self.login)[1]

        request_refresh = {'refresh_token': f'{data["refresh_token"]}'}

        response, refresh_data = self.request(request_refresh, self.refresh)

        self.assertEqual(200, response.status_code)
        self.assertEqual(['access_token'], list(refresh_data.keys()))

    def test_protected_route(self):
        request_jwt = {"email": "test@mail.ru", "password": "test"}

        data = self.request(request_jwt, self.login)[1]

        request_access = {'access_token': f'{data["access_token"]}'}

        response, access_data = self.request(request_access, self.protected, 'get')

        self.assertEqual(200, response.status_code)
        self.assertEqual({'logged_in_as': f'{request_jwt["email"]}'}, access_data)
