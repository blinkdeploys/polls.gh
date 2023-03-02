from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



class User(AbstractUser):
    password = models.CharField(max_length=128)
    username = models.CharField(_("Username"), unique=True, max_length=150)
    first_name = models.CharField(_("First name"), max_length=150)
    last_name = models.CharField(_("Last name"), max_length=150)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField("Date joined", null=True)
    last_login = models.DateTimeField("Last login", null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    is_staff = models.BooleanField(blank=True, null=True)
    is_superuser = models.BooleanField(blank=True, null=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    class Meta:
        db_table = 'account_user'

    def __str__(self):
        return "{} {}".format(self.first_name, self.email)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)