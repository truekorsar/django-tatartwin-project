from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class TatarUser(AbstractUser):
    email = models.EmailField(max_length=254, null=True)

    objects = UserManager()

    class Meta:
        db_table = 'auth_user'





