from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    # password = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=200, null=True)
    registered_date = models.DateTimeField(auto_now_add=True)

    avatar = models.ImageField(upload_to='images/', null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name
