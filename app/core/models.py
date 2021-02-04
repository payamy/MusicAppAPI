import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.contrib.postgres.fields import CICharField

from django.utils.translation import gettext_lazy as _

from django.conf import settings


def advertisement_image_file_path(instance, filename):
    """Generate new file path for ad image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('upload/advertisement/', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password, user_type, **extra_fields):
        """Create and save a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and save a new super user"""
        user = self.create_user(email, password, User.Types.STAFF)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email instead of username"""

    class Types(models.TextChoices):
        STUDENT = 1
        TEACHER = 2
        STAFF = 3

    user_type = models.CharField(_('Type'), max_length=50, choices=Types.choices, default=Types.STUDENT)

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    biography = models.CharField(max_length=255, default='no information')

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Advertisement(models.Model):
    """Ads that each user can post"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    caption = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=advertisement_image_file_path)
    tags = models.ManyToManyField('Tag')
    categories = models.ManyToManyField('Category')


class Classroom(models.Model): 
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='classroom'
    )

    name = models.CharField(max_length=255, blank=False, default='-')
    description = models.CharField(max_length= 255, blank= False, default='-')
    

class Tutorial(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name='tutorials',
        default=1
    )
    title = models.CharField(max_length=255, blank=False, default='-')
    description = models.CharField(max_length=255, blank=False, default='-')
    video = models.FileField(upload_to='videos/', null=True, verbose_name="")
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title + ": " + str(self.video)


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name='comments',
        default=1
    )
    text = models.CharField(max_length=255, blank=False, default='-')
    likes = models.IntegerField(default=0)


class Questionnarie(models.Model):
    Type = User.Types
    title = models.CharField(max_length=300)


class Question(models.Model):
    questionnarie = models.ForeignKey(
        Questionnarie,
        on_delete=models.CASCADE,
        related_name='questionnarie'
        )
    text = models.CharField(max_length=500)
    choice_type = models.CharField(max_length=10) 

class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='question'
        )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )
    answer = models.CharField(max_length=20)
    fileAnswer = models.FileField(upload_to='choicesFiles/', null=True, verbose_name="")

    def __str__(self):
        return self.answer + ": " + str(self.fileAnswer)

    def give_choices(self,ANSWER_CHOICES):
        self.answer=models.CharField(max_length=20,choices=ANSWER_CHOICES)

class Tag(models.Model):
    """Helper model for tagging ads"""
    title = models.CharField(max_length=255, primary_key=True)

    def clean(self):
        self.title = self.title.lower()
    
    def __str__(self):
        return self.title

    def save(self, **kwargs):
        self.clean()
        return super(Tag, self).save(**kwargs)


class Category(models.Model):
    """Helper model for categorizing ads"""
    title = models.CharField(max_length=255, primary_key=True)

    def clean(self):
        self.title = self.title.lower()
    
    def __str__(self):
        return self.title

    def save(self, **kwargs):
        self.clean()
        return super(Category, self).save(**kwargs)


class DirectMessage(models.Model):
    """Direct message model between two users"""
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1,
        related_name='sender'
    )
    reciever = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=2,
        related_name='reciever'
    )
    text = models.CharField(max_length=255, blank=False, default='-')
    datetime = models.DateTimeField(_(""), auto_now=False, auto_now_add=True)

    def clean(self):
        self.text = self.text.strip()

    def save(self, **kwargs):
        self.clean()
        return super(DirectMessage, self).save(**kwargs)


class Chat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    interactors = models.ManyToManyField('User')

