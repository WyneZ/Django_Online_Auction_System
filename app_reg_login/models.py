from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    user_email = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    nrc_no = models.CharField(max_length=150, null=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=500, null=True)
    user_password = models.CharField(max_length=100)
    registered_date = models.DateTimeField(auto_now_add=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    coin_amount = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        managed = True


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
    item_name = models.CharField(max_length=200, null=True)
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
    buyer_nrc = models.CharField(max_length=50, null=True)
    buyer_ph = models.CharField(max_length=20, null=True)
    coin_amount = models.IntegerField(default=0)
    invoice_no = models.CharField(max_length=100, null=True)
    payment_method = models.CharField(max_length=50, null=False)
    invoice_img = models.ImageField(null=True)
    buying_time = models.DateTimeField(auto_now_add=True)

    # coin in/out
    status = models.CharField(max_length=10, null=True)

    class Meta:
        ordering = ['-buying_time']


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


class Advertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    place = models.CharField(max_length=20, null=True)
    ad_coin = models.IntegerField(null=True)
    ad_post_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-ad_post_date']


