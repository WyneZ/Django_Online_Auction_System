from django import forms
from django.forms import ModelForm

from .models import User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('profile_pic',)
        # fields = '__all__'


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'phone', 'address']