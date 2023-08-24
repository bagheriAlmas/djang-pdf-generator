from django.contrib.auth.models import AbstractUser
from django.db import models

USER_GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female')
)


class CustomUser(AbstractUser):
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=USER_GENDER, default='male')

    def __str__(self):
        return self.username
