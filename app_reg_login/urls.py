from django.urls import path
from app_reg_login.views import MyView
from . import views


urlpatterns = [
    path('', MyView.as_view(), name='home'),
    path('register/', views.signup, name='register'),
    path('login/', views.loginUser, name='login'),
]