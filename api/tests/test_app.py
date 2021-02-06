import unittest
from flask import json

from app import app
from clear_db import clear_db
from func.registration import auth_path


clear_db(auth_path)


class TestBase(unittest.TestCase):

    def request(self, text):
        response = app.test_client().post('/api/v1/users/',
                                          data=json.dumps(text),
                                          content_type='application/json',
                                          )
        data = json.loads(response.get_data(as_text=True))
        print('\n' + '-------------------------------------------------------------------------')
        print('-------------------------------------------------------------------------')
        print(text)
        print(data, response.status_code)
        print('-------------------------------------------------------------------------')
        print('-------------------------------------------------------------------------')

        return response, data


class TestRegistration(TestBase):

    def test_begin_valid(self):
        request_json = {"email": "tests@mail.ru", "password": "qwerty78"}

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], "User has been registered")

    def test_double(self):
        request_json = {"email": "tests@mail.ru", "password": "qwerty789012345678901234567890"}

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'mail': 'User already exists'})

    def test_startswith_space_mail(self):
        request_json = {"email": " test3@mail.ru", "password": "qwerty789012345"}

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], "User has been registered")

    def test_starts_endswith_space_mail(self):
        request_json = {"email": " test4@mail.ru ", "password": "qwerty432#%3fdDFG"}

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], "User has been registered")

    def test_endswith_space_mail(self):
        request_json = {"email": "test5@mail.ru ", "password": "qwerty432#%3fdDFG"}

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], "User has been registered")

    def test_psw_short_no_tld(self):
        request_json = {"email": "test6@mail", "password": "qwerty7"}

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'password': 'Password must be 8 - 30 symbols long',
                                          'email': 'Incorrect email'})

    def test_no_at_mail(self):
        request_json = {"email": "test7mail.ru", "password": "qwerty432#%3fdDFG"}

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'email': 'Incorrect email'})

    def test_no_dot_mail(self):
        request_json = {"email": "test8@mail.com", "password": "1234567890123456789012345678901"}

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'password': 'Password must be 8 - 30 symbols long'})

    def test_psw_no_chars(self):
        request_json = {"email": "test9@mail.com", "password": ""}

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'password': 'Password must be 8 - 30 symbols long'})

    def test_no_dot_no_at_mail(self):
        request_json = {"email": "test10mailcom", "password": "456789012345678901"}

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'email': 'Incorrect email'})

    def test_comma_instead_dot_mail(self):
        request_json = {"email": "test11@mail,com", "password": "112345678901"}

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'email': 'Incorrect email'})

    def test_comma_instead_at_mail(self):
        request_json = {"email": "test12,mail.com", "password": "456789012345678901"}

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'email': 'Incorrect email'})

    @classmethod
    def tearDownClass(cls):
        clear_db(auth_path)


if __name__ == '__main__':
    unittest.main()

