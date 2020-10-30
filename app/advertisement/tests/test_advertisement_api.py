from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import User, Advertisement

from advertisement.serializers import AdvertisementSerializer


ADVERTISEMENT_URL = reverse('advertisement:advertisement-list')


def sample_ad(user, **params):
    """Create and return a sample ad"""
    defaults = {
        'caption': 'Brand new post!!'
    }
    defaults.update(params)

    return Advertisement.objects.create(user=user, **defaults)


class PublicAdvertisementAPITest(TestCase):
    """Test unauthorized ad API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(ADVERTISEMENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class ForbiddenAdvertisementAPITest(TestCase):
    """Test student ad API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='student@mail.com',
            password='stu12345',
            name='Fake student',
            user_type=User.Types.STUDENT
        )
        self.client.force_authenticate(self.user)
        
    def test_student_api_access(self):
        """Test if a student user could post (couldn't)"""
        res = self.client.get(ADVERTISEMENT_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_ad_forbidden(self):
        """Test creating an ad by student user"""
        res = self.client.post(ADVERTISEMENT_URL, {'caption': 'my brand new Post!!'})

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateAdvertisementAPITest(TestCase):
    """Test authorized API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='teacher@mail.com',
            password='teacher12345',
            name='Fake teacher',
            user_type=User.Types.TEACHER
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ads(self):
        """Test retrieving list of ads"""
        sample_ad(user=self.user)
        sample_ad(user=self.user)

        res = self.client.get(ADVERTISEMENT_URL)

        ads = Advertisement.objects.all().order_by('-id')
        serializer = AdvertisementSerializer(ads, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ads_limited_to_user(self):
        """Test retrieving ads for user"""
        user2 = get_user_model().objects.create_user(
            email='user2@mail.com',
            password='secondpass',
            name='User2',
            user_type=User.Types.TEACHER
        )
        sample_ad(user=user2)
        sample_ad(user=self.user)

        res = self.client.get(ADVERTISEMENT_URL)

        ads = Advertisement.objects.filter(user=self.user)
        serializer = AdvertisementSerializer(ads, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_create_ad(self):
        """Test creating an ad by teacher user"""
        payload = {
            'caption': 'my brand new Post!!',
        }
        res = self.client.post(ADVERTISEMENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        ad = Advertisement.objects.get(id=res.data['id'])
        self.assertEqual(payload['caption'], getattr(ad, 'caption'))
