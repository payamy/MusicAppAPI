from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

from django.utils.translation import gettext_lazy as _



class UserManager(BaseUserManager):

    def create_user(self, email, password, user_type, **extra_fields):
        """Create and save a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and save a new super user"""
        user = self.create_user(email, password, User.Types.STAFF)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    """Custom user model with email instead of username"""

    class Types(models.TextChoices):
        STUDENT = 1
        TEACHER = 2
        STAFF = 3

    type = models.CharField(_('Type'), max_length=50, choices=Types.choices, default=Types.STUDENT)

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    biography = models.CharField(max_length=255, default='no information')

    objects = UserManager()

    USERNAME_FIELD = 'email'