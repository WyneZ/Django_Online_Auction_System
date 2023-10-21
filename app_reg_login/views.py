from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm

from .forms import MyUserCreationForm
from .models import User

# for login required to enter home
from django.contrib.auth import authenticate, login, logout


# @login_required(login_url='login')
class MyView(View):

    def get(self, request):
        user = User.objects.all()
        print('home>> get:', request.GET, 'post:', request.POST, 'user:', user[0].email)
        context = {'user': user}
        return render(request, 'app_reg_login/home.html', context)

    # def get(self, request):
    #
    #     user = User.objects.get(id=pk)
    #     context = {'user', user}
    #     return render(request, 'app_reg_login/home.html', context)

    # this is for Logout button
    def post(self, request):
        # user = User.objects.all()
        # print('Home POST:', user)
        # context = {'user': user}
        # return render(request, 'app_reg_login/home.html', context)

        logout(request)
        return redirect('login')


def signup(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        print("Ok signUp")
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            sec_form = MyUserCreationForm(request.POST, request.FILES, instance=request.user)
            sec_form.save()
            print(f'Name: {user.name} '
                  f'Email: {user.email} '
                  f'Phone: {user.phone} '
                  f'Avatar: {user.avatar}')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurs during signup')

    context = {'form': form}
    return render(request, 'app_reg_login/reg_login.html', context)


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print('67 inputEmail & pw', email, password)
        try:
            user = User.objects.get(email=email)
            print('65 login:', user.password, 'requestUser:', request.POST)
        except:
            print("User Not Found!!!!!!!!!!!!!!!!!!!!!!")

        user = authenticate(request, email=email, password=password)
        print('authenticated >>', user)
        # users = User.objects.all()
        # for u in users:
        #     print('compare pw:', u.password, password)
        #     if u.email == email and u.password == password:
        #         print(78, u.name)
        #         user = u
        #     else:
        #         return redirect('login')

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print('54 Login Error@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    context = {'page': page}
    return render(request, 'app_reg_login/reg_login.html', context)
