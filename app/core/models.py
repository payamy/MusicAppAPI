from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

from django.utils.translation import gettext_lazy as _

from django.conf import settings


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