from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class TodoViewTest(TestCase):
    fixtures = ['dump.json']

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

    # УТОЧНИТЬ
    def test_api_view_allowed_if_logged_in(self):
        header = {
            'HTTP_AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE2MTU2MjgwLCJqdGkiOiI4MDExNDRkMzM4NTQ0MDg5OTAzYzlhZTI2Y2M1ZDFiYiIsInVzZXJfaWQiOjJ9.rNlZ5JJf2oBaKO8nl8LHizd7wUZYk4rl0-1WcDmp6uo'}
        response = self.client.get('/api/', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
# УТОЧНИТЬ
