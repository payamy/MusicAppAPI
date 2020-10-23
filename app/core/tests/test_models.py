from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    
    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = "payamyarandi@gmail.com"
        password = "PayamPayam123"
        user_type = models.User.Types.STUDENT
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            user_type=user_type
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_checking_type(self):
        email = "payamyarandi@gmail.com"
        password = "PayamPayam123"
        user_type = models.User.Types.STUDENT
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            user_type=user_type
        )

        self.assertEqual(user.type, models.User.Types.STUDENT)
        self.assertNotEqual(user.type, models.User.Types.TEACHER)
