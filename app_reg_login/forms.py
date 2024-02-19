from django import forms
from django.forms import ModelForm

from .models import User, Item, ImageTable, Transition
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'email', 'password1', 'password2', 'nrc_no', 'phone', 'address']
        # fields = '__all__'


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'phone', 'address']


class SellForm(ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'number_of_items', 'country_of_origin', 'estimated_era', 'item_condition', 'reverse_price', 'once_up']

        # seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
        # participants = models.ManyToManyField(User, related_name='participants', blank=True)
        #
        # liked_users = models.ManyToManyField(User, related_name='liked_users', blank=True)
        # like_count = models.IntegerField(default=0)
        #
        # category = models.CharField(max_length=100, null=True)
        # title = models.CharField(max_length=100, null=False)
        # # item_name = models.CharField(max_length=200, null=False)
        # description = models.TextField(null=True, blank=True)
        # number_of_items = models.IntegerField(default=1, null=True)
        # estimated_era = model.CharField(default=None, null=True)
        # item_condition = models.CharField(max_length=100, null=True, blank=False)
        # reverse_price = models.IntegerField(null=False)
        # sell_price = models.IntegerField(null=True, default=0)
        # post_date = models.DateTimeField(auto_now_add=True)
        # due_date = models.CharField(max_length=100, null=True)
        # winner = models.CharField(max_length=50, null=True)


class ImageForm(ModelForm):
    images = forms.FileField()

    class Meta:
        model = ImageTable
        fields = ['images']


class TransitionForm(ModelForm):
    class Meta:
        model = Transition
        fields = ['coin_amount', 'invoice_no', 'payment_method', 'invoice_img']
