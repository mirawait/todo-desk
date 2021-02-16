from django.test import TestCase
import users.models as models


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


class UserModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        models.User.objects.create(username='user', email='email@email.email')

    def test_username_label(self):
        user = models.User.objects.get(username='user')
        label = user._meta.get_field('username').verbose_name
        self.assertEqual(label, 'username')

    def test_email_label(self):
        user = models.User.objects.get(username='user')
        label = user._meta.get_field('email').verbose_name
        self.assertEqual(label, 'email')

    def test_username_max_length(self):
        user = models.User.objects.get(username='user')
        max_length = user._meta.get_field('username').max_length
        self.assertEqual(max_length, 50)

    def test_object_name_is_username(self):
        user = models.User.objects.get(username='user')
        self.assertEqual(user.username, str(user))
