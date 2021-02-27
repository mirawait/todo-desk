from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.utils import json

import todo.models as models
import re


class TodoViewTest(TestCase):
    fixtures = ['dump.json']
    header = {
        'HTTP_AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE2MTU2MjgwLCJqdGkiOiI4MDExNDRkMzM4NTQ0MDg5OTAzYzlhZTI2Y2M1ZDFiYiIsInVzZXJfaWQiOjJ9.rNlZ5JJf2oBaKO8nl8LHizd7wUZYk4rl0-1WcDmp6uo'}

    @classmethod
    def setUpTestData(cls):
        models.Task.objects.create(title='test1',
                                   description='user2@user.user',
                                   date_end='2021-06-10 10:22',
                                   status='Completed',
                                   slug='test1')
        models.Task.objects.create(title='test2',
                                   description='user2@user.user',
                                   date_end='2021-06-10 10:22',
                                   status='Completed',
                                   slug='test2')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_uses_correct_template(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'home.html')

    def test_view_tasks_loaded(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('tasks' in response.context)

    # --------------------------------------------------------------------- #
    def test_api_view_url_exists_at_desired_location(self):
        response = self.client.get('/api/')
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_view_restricted_if_not_logged_in(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_view_get_method_without_slug(self):
        response = self.client.get('/api/', **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_str = response.content.decode()
        self.assertTrue('"title":"test2"' in response_str)
        self.assertTrue('"title":"test1"' in response_str)
        self.assertTrue('"fact":' in response_str)
        self.assertTrue('"weather":' in response_str)
        self.assertTrue('"curr_temp":' in response_str)
        self.assertTrue('"feels_like":' in response_str)
        self.assertTrue('"cloudiness":' in response_str)
        self.assertEqual(len([m.start() for m in re.finditer('"description":"user2@user.user"', response_str)]),
                         2)
        self.assertEqual(len([m.start() for m in re.finditer('"date_end":"2021-06-10T10:22:00\+07:00"', response_str)]),
                         2)

    def test_api_view_get_method_with_slug(self):
        response = self.client.get('/api/test2/', **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_str = response.content.decode()
        self.assertTrue('"title":"test2"' in response_str)
        self.assertTrue('"description":"user2@user.user"' in response_str)
        self.assertTrue('"date_end":"2021-06-10T10:22:00+07:00"' in response_str)
        self.assertTrue('"fact":' in response_str)
        self.assertTrue('"weather":' in response_str)
        self.assertTrue('"curr_temp":' in response_str)
        self.assertTrue('"feels_like":' in response_str)
        self.assertTrue('"cloudiness":' in response_str)

    def test_api_view_post_method(self):
        json_str = {
            "task": {
                    "title": "test3",
                    "description": "user2@user.user",
                    "date_end": "2021-06-10 10:22",
                    "status": "Completed"
            }
        }
        response = self.client.post('/api/',json.dumps(json_str),content_type="application/json", **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode(), '{"success":"Task \'test3\' created successfully"}')

    def test_api_view_put_method_request_not_by_author_or_admin(self):
        json_str = {
            "task": {
                "title": "test2 put",
                "description": "user2@user.user",
                "date_end": "2021-06-10 10:22",
                "status": "Completed"
            }
        }
        response = self.client.put('/api/test2/', json.dumps(json_str), content_type="application/json", **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode(), '{"error":"You don\'t have permission"}')

    def test_api_view_put_method_request_by_admin(self):
        header_admin = {'HTTP_AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE3MDIzODA3LCJqdGkiOiJhZDY3Yzk2NWRhY2M0ODY3YWI4OGI2NWNhNzU1NTQwOSIsInVzZXJfaWQiOjF9.AKNrux-bCITt04OTlF1omd2gHnDbsoDJDb12Lxpj3cU'}
        json_str = {
            "task": {
                "title": "test2 put",
                "description": "user2@user.user",
                "date_end": "2021-06-10 10:22",
                "status": "Completed"
            }
        }
        response = self.client.put('/api/test2/', json.dumps(json_str), content_type="application/json", **header_admin)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode(), '{"success":"Task \'test2 put\' was updated"}')

    def test_api_view_put_method_request_by_author(self):
        header_author = {
            'HTTP_AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE2MTU2MjgwLCJqdGkiOiI4MDExNDRkMzM4NTQ0MDg5OTAzYzlhZTI2Y2M1ZDFiYiIsInVzZXJfaWQiOjJ9.rNlZ5JJf2oBaKO8nl8LHizd7wUZYk4rl0-1WcDmp6uo'}
        json_str = {
                    "task": {
                        "title": "test3",
                        "description": "user2@user.user",
                        "date_end": "2021-06-10 10:22",
                        "status": "Completed"
                    }
        }
        response = self.client.post('/api/', json.dumps(json_str), content_type="application/json", **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_str = {
                    "task": {
                        "title": "test3 put",
                        "description": "user2@user.user",
                        "date_end": "2021-06-10 10:22",
                        "status": "Completed"
                    }
        }
        response = self.client.put('/api/test3/', json.dumps(json_str), content_type="application/json", **header_author)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode(), '{"success":"Task \'test3 put\' was updated"}')

    # УТОЧНИТЬ
    def test_api_view_allowed_if_logged_in(self):
        response = self.client.get('/api/', **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    # УТОЧНИТЬ
