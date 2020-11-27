from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Comment, User, Classroom

from classroom.serializers import CommentSerializer, ClassroomSerializer


COMMENT_URL = reverse('classroom:comment-list')
CLASSROOM_URL = reverse('classroom:classroom-list')


def sample_classroom():
    """Create a sample classroom"""
    return Classroom.objects.create(
        name='myClass',
        owner=get_user_model().objects.create_user(
            email='teacher2@mail.com',
            password='teacher12345',
            name='Fake teacher 2',
            user_type=User.Types.TEACHER
        ),
        description='my first piano lesson'
    )


def sample_comment(user, classroom, **params):
    """Create and return a sample ad"""
    defaults = {
        'text': 'Good class',
    }
    defaults.update(params)

    return Comment.objects.create(user=user, classroom=classroom, **defaults)


class PublicCommentAPITest(TestCase):
    """Test unauthorized comment API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(COMMENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCommentAPITest(TestCase):
    """Test authorized API access"""
    classroom = None

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='teacher@mail.com',
            password='teacher12345',
            name='Fake teacher',
            user_type=User.Types.TEACHER
        )
        self.client.force_authenticate(self.user)
        self.client.post(CLASSROOM_URL, format='json')

        self.user = get_user_model().objects.create_user(
            email='student@mail.com',
            password='student12345',
            name='Fake student',
            user_type=User.Types.STUDENT
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_comment(self):
        """Test retrieving list of ads"""
        sample_comment(user=self.user, classroom=sample_classroom())

        res = self.client.get(COMMENT_URL)

        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
