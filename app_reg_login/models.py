from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    user_email = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    nrc_no = models.CharField(max_length=150, null=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=500, null=True)
    password = models.CharField(max_length=100)
    registered_date = models.DateTimeField(auto_now_add=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    coin_amount = models.IntegerField(default=0)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    # def __str__(self):
    #     return self.name

    class Meta:
        managed = False


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)

    liked_users = models.ManyToManyField(User, related_name='liked_users', blank=True)
    like_count = models.IntegerField(default=0)

    category = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=100, null=False)
    # item_name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True, blank=True)
    number_of_items = models.IntegerField(default=1, null=True)
    estimated_era = models.CharField(max_length=20, null=True)
    country_of_origin = models.CharField(max_length=50, null=True)
    item_condition = models.CharField(max_length=100, null=True, blank=False)
    reverse_price = models.IntegerField(null=False)
    once_up = models.IntegerField(null=False, default=0)
    sell_price = models.IntegerField(null=True, default=0)
    post_date = models.DateTimeField(auto_now_add=True)
    due_date = models.CharField(max_length=100, null=True)
    winner = models.CharField(max_length=50, null=True)

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        return self.title


class ImageTable(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to='images/', null=False)


class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


class Transition(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    coin_amount = models.IntegerField(default=0)
    # user_nrc_no = models.CharField(max_length=20, null=False)
    invoice_no = models.CharField(max_length=100, null=False)
    payment_method = models.CharField(max_length=50, null=False)
    invoice_img = models.ImageField(null=False)
    buying_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_no


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text



