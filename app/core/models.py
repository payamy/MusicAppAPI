from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

from enum import Enum


class UserType(Enum):
    STUDENT = 1
    TEACHER = 2
    STAFF = 3

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


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
        user = self.create_user(email, password, UserType.STAFF)
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    """Custom user model with email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    user_type = models.CharField(max_length=255, choices=UserType.choices())

    objects = UserManager()

    USERNAME_FIELD = 'email'
