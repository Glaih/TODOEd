import unittest
from flask import json, url_for
import logging
import os

from app import app
from tests.clear_db import clear_db
from func.registration import DB_PATH


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s:%(message)s',
                    filename='app.log',
                    level=logging.INFO)

char_multiplier = 50


class TestBase(unittest.TestCase):

    def request(self, text):
        with app.test_request_context():
            response = app.test_client().post(url_for('registration'), json=text)
        data = json.loads(response.get_data(as_text=True))

        logger.info(f'REQUEST: {text}')
        logger.info(f'ACTUAL :{response} | {data}')

        return response, data

    def splitter(self):
        logger.info('-' * char_multiplier)
        logger.info('*' * char_multiplier)
        logger.info('-' * char_multiplier)


class TestRegistration(TestBase):
    @classmethod
    def setUpClass(cls):
        TestBase.splitter(cls)
        clear_db(DB_PATH)
        logger.info(f'DB CLEARED: {os.path.abspath(DB_PATH)}')
        logger.info(f'TESTING START')
        TestBase.splitter(cls)

    def setUp(self):
        logger.info('-' * char_multiplier)

    def tearDown(self):
        logger.info('-' * char_multiplier)

    def test_begin_valid(self):
        request_json = {"email": "tests@mail.ru", "password": "qwerty78"}
        response, data = TestBase.request(self, request_json)

        logger.info(f"EXPECTED: 'success': 'User has been registered', 200")

        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["success"], "User has been registered")
            logger.info('PASSED!')
        except AssertionError:
            logger.exception('FAILED!')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["success"], "User has been registered")

    def test_double(self):
        request_json = {"email": "tests_doouble@mail.ru", "password": "qwerty789012345678901234567890"}
        TestBase.request(self, request_json)
        response, data = TestBase.request(self, request_json)

        logger.info(f"EXPECTED: 'errors': 'mail': 'User already exists', 400")

        try:
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["errors"], {'mail': 'User already exists'})
            logger.info('PASSED!')
        except AssertionError:
            logger.exception('FAILED!')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["errors"], {'mail': 'User already exists'})

    def test_startswith_space_mail(self):
        request_json = {"email": " test3@mail.ru", "password": "qwerty789012345"}
        response, data = TestBase.request(self, request_json)

        logger.info(f"EXPECTED: 'success': 'User has been registered', 200")

        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["success"], "User has been registered")
            logger.info('PASSED!')
        except AssertionError:
            logger.exception('FAILED!')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["success"], "User has been registered")

    def test_starts_endswith_space_mail(self):
        request_json = {"email": " test4@mail.ru ", "password": "qwerty432#%3fdDFG"}
        response, data = TestBase.request(self, request_json)

        logger.info(f"EXPECTED: 'success': 'User has been registered', 200")

        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["success"], "User has been registered")
            logger.info('PASSED!')
        except AssertionError:
            logger.exception('FAILED!')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["success"], "User has been registered")

    def test_endswith_space_mail(self):
        request_json = {"email": "test5@mail.ru ", "password": "qwerty432#%3fdDFG"}
        response, data = TestBase.request(self, request_json)

        logger.info(f"EXPECTED: 'success': 'User has been registered', 200")

        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["success"], "User has been registered")
            logger.info('PASSED!')
        except AssertionError:
            logger.exception('FAILED!')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["success"], "User has been registered")

    def test_psw_short_no_tld(self):
        request_json = {"email": "test6@mail", "password": "qwerty7"}
        response, data = TestBase.request(self, request_json)

        logger.info(f"EXPECTED: 'errors': 'password': 'Password must be 8 - 30 symbols long', "
                    f"'email': 'Incorrect email', 200")

        try:
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["errors"], {'password': 'Password must be 8 - 30 symbols long',
                                              'email': 'Incorrect email'})
            logger.info('PASSED!')
        except AssertionError:
            logger.exception('FAILED!')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["errors"], {'password': 'Password must be 8 - 30 symbols long',
                                              'email': 'Incorrect email'})

    def test_no_at_mail(self):
        request_json = {"email": "test7mail.ru", "password": "qwerty432#%3fdDFG"}
        response, data = TestBase.request(self, request_json)

        logger.info(f"EXPECTED: 'errors': 'email': 'Incorrect email'")

        try:
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["errors"], {'email': 'Incorrect email'})
            logger.info('PASSED!')
        except AssertionError:
            logger.exception('FAILED!')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["errors"], {'email': 'Incorrect email'})

    def test_no_dot_mail(self):
        request_json = {"email": "test8@mail.com", "password": "1234567890123456789012345678901"}
        response, data = TestBase.request(self, request_json)

        logger.info(f"EXPECTED: 'errors': 'password': 'Password must be 8 - 30 symbols long'")

        try:
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["errors"], {'password': 'Password must be 8 - 30 symbols long'})
            logger.info('PASSED!')
        except AssertionError:
            logger.exception('FAILED!')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["errors"], {'password': 'Password must be 8 - 30 symbols long'})

    def test_psw_no_chars(self):
        request_json = {"email": "test9@mail.com", "password": ""}
        response, data = TestBase.request(self, request_json)

        logger.info(f"EXPECTED: 'errors': 'password': 'Password must be 8 - 30 symbols long'")

        try:
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["errors"], {'password': 'Password must be 8 - 30 symbols long'})
            logger.info('PASSED!')
        except AssertionError:
            logger.exception('FAILED!')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["errors"], {'password': 'Password must be 8 - 30 symbols long'})

    def test_no_dot_no_at_mail(self):
        request_json = {"email": "test10mailcom", "password": "456789012345678901"}
        response, data = TestBase.request(self, request_json)

        logger.info(f"EXPECTED: 'errors': 'email': 'Incorrect email'")

        try:
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["errors"], {'email': 'Incorrect email'})
            logger.info('PASSED!')
        except AssertionError:
            logger.exception('FAILED!')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["errors"], {'email': 'Incorrect email'})

    def test_comma_instead_dot_mail(self):
        request_json = {"email": "test11@mail,com", "password": "112345678901"}
        response, data = TestBase.request(self, request_json)

        logger.info(f"EXPECTED: 'errors': 'email': 'Incorrect email'")

        try:
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["errors"], {'email': 'Incorrect email'})
            logger.info('PASSED!')
        except AssertionError:
            logger.exception('FAILED!')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["errors"], {'email': 'Incorrect email'})

    def test_comma_instead_at_mail(self):
        request_json = {"email": "test12,mail.com", "password": "456789012345678901"}
        response, data = TestBase.request(self, request_json)

        logger.info(f"EXPECTED: 'errors': 'email': 'Incorrect email'")

        try:
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["errors"], {'email': 'Incorrect email'})
            logger.info('PASSED!')
        except AssertionError:
            logger.exception('FAILED!')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["errors"], {'email': 'Incorrect email'})

    def test_not_json(self):
        request_json = 'not JSON'
        response, data = TestBase.request(self, request_json)

        logger.info(f"EXPECTED: 'type_error': 'data must be in json format', 400")

        try:
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["type_error"], "data must be in json format")
            logger.info('PASSED!')
        except AssertionError:
            logger.exception('FAILED!')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["type_error"], "data must be in json format")

    def test_wrong_keys(self):
        request_json = {"passworddd": "qwerty78"}
        response, data = TestBase.request(self, request_json)

        logger.info(f"EXPECTED: 'json_key_error': 'wrong keys', 200")

        try:
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["json_key_error"], "wrong keys")
            logger.info('PASSED!')
        except AssertionError:
            logger.exception('FAILED!')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["json_key_error"], "wrong keys")

    @classmethod
    def tearDownClass(cls):
        TestBase.splitter(cls)
        logger.info(f'TESTING END')
        clear_db(DB_PATH)
        logger.info(f'DB CLEARED: {os.path.abspath(DB_PATH)}')
        TestBase.splitter(cls)


if __name__ == '__main__':
    unittest.main()

