from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import ugettext_lazy as _
# need to check out meaning #


class MyUserManager(UserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('You must enter an email address')

        user = self.model(
            email=self.normalize_email(email),
            # lowercapital #
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if not email:
            raise ValueError('You must enter an email address')
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    #  """verbose_name --> _"""
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
