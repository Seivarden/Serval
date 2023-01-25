from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from .managers import CustomUserManager

from django.urls .base import reverse

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length = 100, blank=True)
    last_name = models.CharField(_('last name'), max_length = 100, blank=True)
    national_id_num = models.IntegerField(blank=True, null=True)
    national_id_front = models.ImageField(blank=True, null=True)
    national_id_back = models.ImageField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = CustomUserManager()

    def __str__(self):
        return f'{ self.first_name } { self.last_name }'

    def get_absolute_url(self):
        return(reverse('user-detail', args=[str(self.id)]))

    