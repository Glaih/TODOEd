import unittest
import logging
import datetime
from flask import url_for
from bcrypt import checkpw
from datetime import timedelta
from time import sleep

from core import create_app
from core.database import User, Task, db

logger = logging.getLogger(__name__)

app = create_app(test_config=True)


class TestBase(unittest.TestCase):
    @staticmethod
    def request(json_data, endpoint, method='post'):
        client = app.test_client()
        method_func = client.post if method == 'post' else client.get
        with app.test_request_context():
            url = url_for(endpoint)
            response = method_func(url, json=json_data)
        data = response.get_json()

        return response, data


class TestRegistrationErrors(TestBase):
    def setUp(self):
        self.endpoint = 'api.create_user'

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
        self.assertEqual({'type_error': "'int' object is not subscriptable"}, data["errors"])

    def test_wrong_keys(self):
        request_json = {"passworddd": "qwerty78"}
        response, data = self.request(request_json, self.endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'json_key_error': 'wrong keys'}, data["errors"])


class TestRegistrationDb(TestBase):

    def setUp(self):
        clear_db(app)
        self.endpoint = 'api.create_user'

    @classmethod
    def tearDownClass(cls):
        clear_db(app)

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
        mail = "test5@mail.ru"

        self.request({"email": "test5@mail.ru ", "password": password}, self.endpoint)
        with app.app_context():
            password_in_db = User.get_one(mail).password

        self.assertTrue(checkpw(password.encode(), password_in_db.encode()))
        self.assertFalse(checkpw(invalid_password.encode(), password_in_db.encode()))


class TestJWT(TestBase):
    @classmethod
    def setUpClass(cls):
        clear_db(app)
        cls.login = 'api.login_user'
        cls.refresh = 'api.refresh_token'
        cls.protected = 'api.protected'
        cls.valid_request = {"email": "testJWT@mail.ru ", "password": 'qWeRtYoneoneone'}
        cls.request(cls.valid_request, 'api.create_user')

    @classmethod
    def tearDownClass(cls):
        clear_db(app)

    def test_login_type_error(self):
        request_json = 21
        response, data = self.request(request_json, self.login)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'type_error': "'int' object is not subscriptable"}, data["errors"])

    def test_login_wrong_keys(self):
        request_json = {"passworddd": "qwerty78"}
        response, data = self.request(request_json, self.login)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'json_key_error': 'wrong keys'}, data["errors"])

    def test_acquire_jwt(self):
        response, data = self.request(self.valid_request, self.login)

        self.assertEqual(200, response.status_code)
        self.assertEqual(['access_token', 'refresh_token'], list(data.keys()))

    def test_acquire_jwt_request_none(self):
        response, data = self.request(None, self.login)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'type_error': "'NoneType' object is not subscriptable"}, data['errors'])

    def test_acquire_jwt_wrong_user(self):
        request_json = {"email": "testo@mail.ru", "password": "test"}

        response, data = self.request(request_json, self.login)

        self.assertEqual(403, response.status_code)
        self.assertEqual({'errors': {'email': 'user does not exist'}}, data)

    def test_acquire_jwt_wrong_password(self):
        request_json = {"email": "testJWT@mail.ru ", "password": 'qWeRtYoneone'}

        response, data = self.request(request_json, self.login)

        self.assertEqual(403, response.status_code)
        self.assertEqual({'errors': {'password': 'incorrect password'}}, data)

    def test_refresh_jwt(self):
        _, data = self.request(self.valid_request, self.login)

        request_refresh = {'refresh_token': data["refresh_token"]}

        response, refresh_data = self.request(request_refresh, self.refresh)

        self.assertEqual(200, response.status_code)
        self.assertEqual(['access_token'], list(refresh_data.keys()))

    def test_refresh_jwt_expired(self):
        app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(milliseconds=1)

        _, data = self.request(self.valid_request, self.login)

        sleep(1)

        request_refresh = {'refresh_token': data["refresh_token"]}

        response, refresh_data = self.request(request_refresh, self.refresh)

        self.assertEqual(401, response.status_code)
        self.assertEqual({'msg': 'Token has expired'}, refresh_data)

        app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(seconds=60)

    def test_refresh_jwt_invalid_dict(self):
        self.request(self.valid_request, self.login)

        request_refresh = {'refresh_token': f'no'}

        response, refresh_data = self.request(request_refresh, self.refresh)

        self.assertEqual(422, response.status_code)
        self.assertEqual({'msg': 'Not enough segments'}, refresh_data)

    def test_refresh_jwt_None(self):
        self.request(self.valid_request, self.login)

        request_refresh = None

        response, refresh_data = self.request(request_refresh, self.refresh)

        self.assertEqual(401, response.status_code)
        self.assertEqual({'msg': 'Invalid content-type. Must be application/json.'}, refresh_data)

    def test_protected_route(self):
        _, data = self.request(self.valid_request, self.login)

        request_access = {'access_token': data["access_token"]}

        response, access_data = self.request(request_access, self.protected, 'get')

        self.assertEqual(200, response.status_code)
        self.assertEqual({'user_id': access_data['user_id']}, access_data)

    def test_protected_route_invalid_jwt_dict(self):

        request_access = {'access_token': 'no'}

        response, access_data = self.request(request_access, self.protected, 'get')

        self.assertEqual(422, response.status_code)
        self.assertEqual({'msg': 'Not enough segments'}, access_data)

    def test_protected_route_invalid_jwt_none(self):

        request_access = None

        response, access_data = self.request(request_access, self.protected, 'get')

        self.assertEqual(401, response.status_code)
        self.assertEqual({'msg': 'Invalid content-type. Must be application/json.'}, access_data)

    def test_protected_route_wrong_jwt(self):
        request_access = {'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxNDY3'
                                          'NTkyNywianRpIjoiNmExOWVmNDYtNDI0NC00NWVkLTk4YTQtYzM1MDU1OGJmY2FhIiwibmJmIj'
                                          'oxNjE0Njc1OTI3LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoidGVzdEBtYWlsLnJ1IiwiZXhwIjox'
                                          'NjE0NzYyMzI3fQ.9oWgnQQQnuY5iAlTPqkuAINqw9II5BMxbEAUucYHLTc'}

        response, access_data = self.request(request_access, self.protected, 'get')

        self.assertEqual(422, response.status_code)
        self.assertEqual({'msg': 'Signature verification failed'}, access_data)

    def test_protected_route_expired_jwt(self):
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(milliseconds=1)

        _, data = self.request(self.valid_request, self.login)

        sleep(1)

        request_access = {'access_token': data["access_token"]}

        response, access_data = self.request(request_access, self.protected, 'get')

        self.assertEqual(401, response.status_code)
        self.assertEqual({'msg': 'Token has expired'}, access_data)

        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=30)


class TestTasks(TestBase):
    @classmethod
    def setUpClass(cls):
        clear_db(app)
        cls.registration_endpoint = 'api.create_user'
        cls.protected = 'api.protected'
        cls.login_endpoint = 'api.login_user'
        cls.add_task_endpoint = 'api.create_task'
        cls.valid_request = {"email": "testJWT@mail.ru ", "password": 'qWeRtYoneoneone'}
        cls.request(cls.valid_request, cls.registration_endpoint)
        _, cls.data = cls.request(cls.valid_request, cls.login_endpoint)
        _, cls.user_id = cls.request(cls.data, cls.protected, method='GET')

    @classmethod
    def tearDownClass(cls):
        clear_db(app)

    def test_task_writen_deadline(self):
        task_add_request = self.data
        task_add_request['data'] = {"title": "test_title", "text": "test_text", "deadline": "2022-02-28T18:31:42+04:30"}
        response, answer = self.request(task_add_request, self.add_task_endpoint)
        created_at = datetime.datetime.utcnow().strftime("%Y.%m.%d %H:%M")

        with app.app_context():
            task_written = Task.get_one(answer['data']['task_id'])

        self.assertEqual(200, response.status_code)
        self.assertEqual(answer['data']['task_id'], task_written.task_id)
        self.assertEqual(self.user_id['user_id'], task_written.user_id)
        self.assertEqual(task_add_request['data']['title'], task_written.title)
        self.assertEqual(task_add_request['data']['text'], task_written.text)
        self.assertEqual(datetime.datetime.fromisoformat(task_add_request['data']['deadline']), task_written.deadline)
        self.assertTrue(created_at, task_written.created_at.strftime("%Y.%m.%d %H:%M"))

    def test_task_written_no_deadline(self):
        task_add_request = self.data
        task_add_request['data'] = {"title": "test_title", "text": "test_text"}
        response, answer = self.request(task_add_request, self.add_task_endpoint)
        created_at = datetime.datetime.utcnow().strftime("%Y.%m.%d %H:%M")

        with app.app_context():
            task_written = Task.get_one(answer['data']['task_id'])

        self.assertEqual(200, response.status_code)
        self.assertEqual(answer['data']['task_id'], task_written.task_id)
        self.assertEqual(self.user_id['user_id'], task_written.user_id)
        self.assertEqual(task_add_request['data']['title'], task_written.title)
        self.assertEqual(task_add_request['data']['text'], task_written.text)
        self.assertTrue(created_at, task_written.created_at.strftime("%Y.%m.%d %H:%M"))
        self.assertEqual(None, task_written.deadline)

    def test_task_add_wrong_key(self):
        task_add_request = self.data
        task_add_request['data'] = {"title": "test_title", "t1ext": "test_text", "deadline": ""}
        response, answer = self.request(task_add_request, self.add_task_endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'errors': {'json_key_error': 'wrong keys'}}, answer)

    def test_task_add_short_text(self):
        task_add_request = self.data
        task_add_request['data'] = {"title": "test_title", "text": "", "deadline": ""}
        response, answer = self.request(task_add_request, self.add_task_endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'errors': {'text': 'Text must be 1-180 chars long'}}, answer)

    def test_task_add_long_text(self):
        task_add_request = self.data
        task_add_request['data'] = {"title": "test_title", "text": f"{'1'*181}", "deadline": ""}
        response, answer = self.request(task_add_request, self.add_task_endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'errors': {'text': 'Text must be 1-180 chars long'}}, answer)

    def test_task_add_short_title(self):
        task_add_request = self.data
        task_add_request['data'] = {"title": "", "text": "test", "deadline": ""}
        response, answer = self.request(task_add_request, self.add_task_endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'errors': {'title': 'Title must be 1-30 chars long'}}, answer)

    def test_task_add_long_title(self):
        task_add_request = self.data
        task_add_request['data'] = {"title": f"{'1' * 31}", "text": "test", "deadline": ""}
        response, answer = self.request(task_add_request, self.add_task_endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'errors': {'title': 'Title must be 1-30 chars long'}}, answer)

    def test_task_add_short_title_short_text(self):
        task_add_request = self.data
        task_add_request['data'] = {"title": "", "text": "", "deadline": ""}
        response, answer = self.request(task_add_request, self.add_task_endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'errors': {'text': 'Text must be 1-180 chars long',
                                     'title': 'Title must be 1-30 chars long'}}, answer)

    def test_task_add_long_title_long_text(self):
        task_add_request = self.data
        task_add_request['data'] = {"title": f"{'1' * 31}", "text": f"{'1'*181}", "deadline": ""}
        response, answer = self.request(task_add_request, self.add_task_endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'errors': {'text': 'Text must be 1-180 chars long',
                                     'title': 'Title must be 1-30 chars long'}}, answer)

    def test_task_add_deadline_from_past(self):
        task_add_request = self.data
        task_add_request['data'] = {"title": "test_title", "text": "test_text", "deadline": "2021-02-28T18:31:42+04:30"}
        response, answer = self.request(task_add_request, self.add_task_endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({"errors": {"deadline": "Deadline cannot be from past"}}, answer)

    def test_task_add_deadline_without_timezone(self):
        task_add_request = self.data
        task_add_request['data'] = {"title": "test_title", "text": "test_text", "deadline": "2021-02-28T18:31:42"}
        response, answer = self.request(task_add_request, self.add_task_endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'errors': {'deadline': 'Deadline must have timezone'}}, answer)

    def test_task_add_deadline_wrong_format(self):
        task_add_request = self.data
        task_add_request['data'] = {"title": "test_title", "text": "test_text", "deadline": "2021/02/28T18:31:42+04:30"}
        response, answer = self.request(task_add_request, self.add_task_endpoint)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'errors': {"deadline": "Invalid isoformat string: '2021/02/28T18:31:42+04:30'"}}, answer)

    def test_task_add_no_user(self):
        task_add_request = self.data
        clear_db(app)
        task_add_request['data'] = {"title": "test_title", "text": "test_text", "deadline": "2022-02-28T18:31:42+04:30"}
        response, answer = self.request(task_add_request, self.add_task_endpoint)

        self.request(self.valid_request, self.registration_endpoint)
        _, self.data = self.request(self.valid_request, self.login_endpoint)
        _, self.user_id = self.request(self.data, self.protected, method='GET')

        self.assertEqual(400, response.status_code)
        self.assertEqual({'errors': {'user_id': f"user_id={self.user_id['user_id']} doesn't exists"}}, answer)

    def test_task_add_deadline_wrong_token(self):
        task_add_request = {
            'data': {"title": "test_title", "text": "test_text", "deadline": "2021/02/28T18:31:42+04:30"},
            'access_token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxOD"
                            "Q4MjY5NCwianRpIjoiNDAwMDUxZmYtOTYyOC00NDFjLWJkNzAtOGVkM2Y0NmM1MzIzIiwib"
                            "mJmIjoxNjE4NDgyNjk0LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoyLCJleHAiOjE2MTg1Njkw"
                            "OTR9.L9agfMTbM-bkLgsIplySMq-rThSpd12cMNno2c5_YzE"}

        response, answer = self.request(task_add_request, self.add_task_endpoint)

        self.assertEqual(422, response.status_code)
        self.assertEqual({'msg': 'Signature verification failed'}, answer)

    def test_task_add_expired_token(self):
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(milliseconds=1)

        _, request = self.request(self.valid_request, self.login_endpoint)
        request['data'] = {"title": "test_title", "text": "test_text", "deadline": "2022-02-28T18:31:42+04:30"}

        sleep(1)

        response, answer = self.request(request, self.add_task_endpoint)

        self.assertEqual(401, response.status_code)
        self.assertEqual({'msg': 'Token has expired'}, answer)

        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=30)

    def test_task_add_deadline_invalid_token(self):
        task_add_request = {
            'data': {"title": "test_title", "text": "test_text", "deadline": "2021/02/28T18:31:42+04:30"},
            'access_token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eykmcmVzaCI6ZmFsc2UsImlhdCI6MTYxOD"
                            "Q4MjY5NCwianRpIjoiNDAwMDUxZmYtOTYy00NDFgLWJkNzAtOGVkM2Y0NmM1MzIzIiwib"
                            "mJmIjoxNjE4NDgyNjk0LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoyLCJleHAiOjE2MTg1Njkw"
                            "OTR9.L9agfMTbM-bkLgsIplySMq-rThSpd12cMNno2c5_YzE"}

        response, answer = self.request(task_add_request, self.add_task_endpoint)

        self.assertEqual(422, response.status_code)
        self.assertIn('Invalid payload string', answer['msg'])


def clear_db(app_instance):
    db.drop_all(app=app_instance)
    db.create_all(app=app_instance)
