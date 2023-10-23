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

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True, blank=True)
    reverse_price = models.IntegerField(max_length=20, null=False)
    item_condition = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    # end_date =

    class Meta:
        ordering = ['-start_date']








