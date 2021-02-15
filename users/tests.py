from django.test import TestCase
from rest_framework import status

import users.models as models
from django.test.client import Client


# Create your tests here.


class UserManagerTestCase(TestCase):
    def test_create_user(self):
        test_user = models.UserManager.create_user(models.User.objects, "UserName",
                                                   "email@email.email", "password")
        self.assertEqual(test_user.username, "UserName")
        self.assertEqual(test_user.email, "email@email.email")
        self.assertEqual(test_user.check_password("password"), True)
        self.assertFalse(test_user.is_staff)
        self.assertTrue(test_user.is_active)
        # call_command('flush')

    def test_create_superuser(self):
        test_user = models.UserManager.create_superuser(models.User.objects, "UserName",
                                                        "email@email.email", "password")
        self.assertEqual(test_user.username, "UserName")
        self.assertEqual(test_user.email, "email@email.email")
        self.assertEqual(test_user.check_password("password"), True)
        self.assertTrue(test_user.is_staff)
        # call_command('flush')


class RegistrationTestClass(TestCase):
    def test_registration(self):
        c = Client()
        response = c.post('/api/users/registration/',
                          {"username": "user7", "email": "email4@email.email", "password1": "qweasdzxc",
                           "password2": "qweasdzxc"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTestClass(TestCase):
    fixtures = ['dump.json']

    def test_login(self):
        c = Client()
        print(models.User.objects.all())
        # c.post('/api/users/registration/',
        #        {"username": "user7", "email": "email4@email.email", "password1": "qweasdzxc",
        #         "password2": "qweasdzxc"})
        response = c.post('/api/users/login/',
                          {"username": "user7", "email": "email4@email.email", "password": "qweasdzxc",
                           "password2": "qweasdzxc"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response = c.login(username='user6', email='email4@email.email', password='qweasdzxc')
