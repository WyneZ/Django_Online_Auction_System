from django import forms
from django.forms import ModelForm

from .models import User, Item, ImageTable, Transition
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'password1', 'password2', 'phone', 'address']
        # fields = '__all__'


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'phone', 'address']


class SellForm(ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'item_name', 'description', 'reverse_price', 'item_condition']


class ImageForm(ModelForm):
    images = forms.FileField()

    class Meta:
        model = ImageTable
        fields = ['images']


class TransitionForm(ModelForm):
    class Meta:
        model = Transition
        fields = ['coin_amount', 'invoice_no', 'payment_method', 'invoice_img']
