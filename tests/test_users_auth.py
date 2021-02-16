from rest_framework import status
from django.test.client import Client
from django.test import TestCase


class RegistrationTestClass(TestCase):
    def test_registration_valid_data(self):
        c = Client()
        response = c.post('/api/users/registration/',
                          {"username": "user7", "email": "email4@email.email", "password1": "qweasdzxc",
                           "password2": "qweasdzxc"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_invalid_data(self):
        c = Client()
        response = c.post('/api/users/registration/',
                          {"username": "user7", "email": "email4@email.email", "password1": "qweasdzxc"})
        self.assertTrue(b'errors' in response.content)


class LoginTestClass(TestCase):
    fixtures = ['dump.json']

    def test_login(self):
        c = Client()
        response = c.post('/api/users/login/',
                          {"username": "user7", "email": "email4@email.email", "password": "qweasdzxc",
                           "password2": "qweasdzxc"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response = c.login(username='user6', email='email4@email.email', password='qweasdzxc')
