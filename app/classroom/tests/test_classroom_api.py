from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Classroom, User

from classroom.serializers import ClassroomSerializer


CLASSROOM_URL = reverse('classroom:myclassroom-list')
PUBLIC_CLASSROOM_URL = reverse('classroom:classroom-list')


def sample_classroom(user, *params):
    """Create and return a sample classroom"""
    defaults = {
        'name': 'My first classroom',
        'description': 'Hi! this is my first Piano lesson.'
    }
    defaults.update(params)

    return Classroom.objects.create(owner=user, **defaults)


class PublicClassroomAPITest(TestCase):
    """Test unauthorized comment API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(CLASSROOM_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class ForbiddenClassroomAPITest(TestCase):
    """Test student classroom API access"""

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
        """Test if a student user could access classrooms"""
        res = self.client.get(CLASSROOM_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.get(PUBLIC_CLASSROOM_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_classroom_forbidden(self):
        """Test creating an classroom by student user"""
        res = self.client.post(CLASSROOM_URL, {'caption': 'my brand new Post!!'})

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateClassroomAPITest(TestCase):
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

    def test_retrieve_classrooms(self):
        """Test retrieving list of classrooms"""
        sample_classroom(user=self.user)
        sample_classroom(user=self.user)

        res = self.client.get(CLASSROOM_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_classrooms_limited_to_user(self):
        """Test retrieving classrooms for user"""
        user2 = get_user_model().objects.create_user(
            email='user2@mail.com',
            password='secondpass',
            name='User2',
            user_type=User.Types.TEACHER
        )
        sample_classroom(user=user2)
        sample_classroom(user=user2)
        sample_classroom(user=self.user)

        res = self.client.get(CLASSROOM_URL)

        classrooms = Classroom.objects.filter(owner=self.user)
        serializer = ClassroomSerializer(classrooms, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_create_classroom(self):
        """Test creating an classroom by teacher user"""
        payload = {
            'name': 'my brand new Class!!',
        }
        res = self.client.post(CLASSROOM_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        classroom = Classroom.objects.get(id=res.data['id'])
        self.assertEqual(payload['name'], getattr(classroom, 'name'))