from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import ugettext_lazy as _
# need to check out meaning #


class MyUserManager(UserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('You must enter an email address')

        user = self.model(
            email=self.normalize_email(email),
            password=password, **kwargs
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
    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class LoginToken(models.Model):
    email = models.EmailField(_('email_address'))
    token_id = models.CharField(max_length=40)
    token_expires = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('magic_confirm', args=[self.token_id])
