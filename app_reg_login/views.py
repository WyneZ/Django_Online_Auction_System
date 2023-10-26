from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm

from .forms import MyUserCreationForm, UserForm, SellForm
from .models import User, Item, Category

# for login required to enter home
from django.contrib.auth import authenticate, login, logout


class MyView(View):

    def get(self, request):
        latest_items = Item.objects.all()
        context = {'latest_items': latest_items}
        return render(request, 'app_reg_login/home.html', context)

    # this is for Logout button
    def post(self, request):
        # user = User.objects.all()
        # print('Home POST:', user)
        # context = {'user': user}
        # return render(request, 'app_reg_login/profile.html', context)

        logout(request)
        return redirect('login')


def signup(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        print("Ok signUp:")
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            user = form.save()
            user.username = user.username.lower()
            user.save()
            print(f'Name: {user.name} '
                  f'Email: {user.email} '
                  f'Phone: {user.phone} ')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurs during signup')

    context = {'form': form}
    return render(request, 'app_reg_login/reg_login_old.html', context)


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


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        logout(request)
        user.delete()
        return redirect('home')

    context = {'user': user}
    return render(request, 'app_reg_login/profile.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user.id)

    context = {'form': form}
    return render(request, 'app_reg_login/updateUser.html', context)


def sellItem(request):
    form = SellForm()
    items = Item.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        form = SellForm(request.POST, request.FILES)
        print('All items:', items)
        print('Sell:', request.POST['category'], type(request.POST['category']))
        if form.is_valid():
            item = form.save()
            item.save()
        # category_name = request.POST.get('category')
        # category, start_date = Category.objects.get_or_create(name=category_name)

        # Item.objects.create(
        #     seller=request.user,
        #     category=request.POST['category'],
        #     title=request.POST['title'],
        #     item_name=request.POST['item_name'],
        #     description=request.POST['description'],
        #     item_image=request.POST['item_image'],
        #     reverse_price=request.POST['reverse_price'],
        #     item_condition=request.POST['item_condition']
        #     # highest_price=request.POST.get('reverse_price'),
        # )
        return redirect('home')
    context = {'form': form}
    return render(request, 'app_reg_login/sell_item.html', context)
