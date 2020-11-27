from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import User, Tag

from advertisement.serializers import TagSerializer

TAG_URL = reverse('advertisement:tag-list')


class TagAPITest(TestCase):
    """Test tag API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='teacher@mail.com',
            password='teacher12345',
            name='Fake teacher',
            user_type=User.Types.TEACHER
        )
        self.client.force_authenticate(self.user)

    def test_create_tag_ci(self):
        """Test if tags are case insensitive"""
        payload = {
            'title': 'piano',
        }
        payload2 = {
            'title': 'piano2',
        }
        res = self.client.post(TAG_URL, payload)
        res2 = self.client.post(TAG_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

        