from app import app
from flask import json
from clear_db import clear_db
import unittest

path = 'api/db/auth.db'
clear_db(path)


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
    def setUp(self):
        pass

    def test_begin_valid(self):
        request_json = {"email": "tests@mail.ru", "password": "qwerty78"}

        print('Test1')

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], "User has been registered")

    def test_double(self):
        request_json = {"email": "tests@mail.ru", "password": "qwerty789012345678901234567890"}

        print('Test2')

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'mail': 'User already exists'})

    def test_fwd_space_mail(self):
        request_json = {"email": " test3@mail.ru", "password": "qwerty789012345"}
        print('Test3')
        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], "User has been registered")

    def test_fwd_end_space_mail(self):
        request_json = {"email": " test4@mail.ru ", "password": "qwerty432#%3fdDFG"}

        print('Test4')

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], "User has been registered")

    def test_end_space_mail(self):
        request_json = {"email": "test5@mail.ru ", "password": "qwerty432#%3fdDFG"}

        print('Test5')

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], "User has been registered")

    def test_psw_short_no_tld(self):
        request_json = {"email": "test6@mail", "password": "qwerty7"}

        print('Test6')

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'password': 'Password must be 8 - 30 symbols long',
                                          'email': 'Incorrect email'})

    def test_no_at_mail(self):
        request_json = {"email": "test7mail.ru", "password": "qwerty432#%3fdDFG"}

        print('Test7')

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'email': 'Incorrect email'})

    def test_no_dot_mail(self):
        request_json = {"email": "test8@mail.com", "password": "1234567890123456789012345678901"}

        print('Test8')

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'password': 'Password must be 8 - 30 symbols long'})

    def test_psw_0(self):
        request_json = {"email": "test9@mail.com", "password": ""}

        print('Test9')

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'password': 'Password must be 8 - 30 symbols long'})

    def test_no_dot_no_at_mail(self):
        request_json = {"email": "test10mailcom", "password": "456789012345678901"}

        print('Test10')

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'email': 'Incorrect email'})

    def test_comma_inst_dot_mail(self):
        request_json = {"email": "test11@mail,com", "password": "112345678901"}

        print('Test11')

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'email': 'Incorrect email'})

    def test_comma_inst_at_mail(self):
        request_json = {"email": "test12,mail.com", "password": "456789012345678901"}

        print('Test12')

        response, data = TestBase.request(self, request_json)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["errors"], {'email': 'Incorrect email'})

    @classmethod
    def tearDownClass(cls):
        clear_db(path)


if __name__ == '__main__':
    unittest.main()

