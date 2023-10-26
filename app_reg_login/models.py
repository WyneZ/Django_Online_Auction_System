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
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=100, null=False)

    category = models.CharField(max_length=100, null=True)

    item_name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True, blank=True)
    item_image = models.ImageField(null=True, default='avatar.svg')
    reverse_price = models.IntegerField(null=False)
    highest_price = models.IntegerField(null=True, default=0)
    item_condition = models.CharField(max_length=100, null=True, blank=False)
    start_date = models.DateTimeField(auto_now_add=True)
    # end_date =

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title








