from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from .forms import MyUserCreationForm, UserForm, SellForm, ImageForm
from .models import User, Category, Item, ImageTable, Bids

# for login required to enter home
from django.contrib.auth import authenticate, login, logout


# Function to get only {item: one image} | not for images
def create_related_dict(item_list, image_list):
    related_dict: dict = {}
    for item in item_list:
        for image in image_list:
            if image.item == item:
                image_dict = {item: image.image_url}
                related_dict.update(image_dict)
                break

    return related_dict


class MyView(View):

    def get(self, request):
        latest_items = Item.objects.all()
        all_images = ImageTable.objects.all()

        # delete image if user account is deleted
        for image in all_images:
            if image.item.seller is None:
                image.delete()

        related_dict = create_related_dict(latest_items, all_images)

        context = {'latest_items': latest_items, "all_images": all_images, "related_dict": related_dict}
        return render(request, 'app_reg_login/home.html', context)

    # this is for Logout button
    def post(self, request):
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
        try:
            user = User.objects.get(email=email)
        except:
            print("User Not Found!!!")

        user = authenticate(request, email=email, password=password)
        print('authenticated >>', user)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print('54 Login Error!!')
    context = {'page': page}
    return render(request, 'app_reg_login/reg_login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id=pk)
    item_list = user.item_set.all()
    images = ImageTable.objects.all()

    related_dict = create_related_dict(item_list, images)

    # auction_history =

    if request.method == 'POST':
        logout(request)
        user.delete()
        return redirect('home')

    context = {'user': user, 'related_dict': related_dict}
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

    if request.method == 'POST':
        form = SellForm(request.POST, request.FILES)
        print('Sell:', request.POST['category'], type(request.POST['category']))

        if form.is_valid():
            item = form.save()
            item.seller = request.user
            item.save()

            images = request.FILES.getlist('upload_images')
            for image in images:
                image = ImageTable.objects.create(
                    item=item,
                    image_url=image
                )
        category_name = request.POST.get('category')
        category, start_date = Category.objects.get_or_create(name=category_name)

        return redirect('home')
    context = {'form': form}
    return render(request, 'app_reg_login/sell_item.html', context)


def item_detail(request, pk):
    item = Item.objects.get(id=pk)
    images = ImageTable.objects.filter(item=item)
    item_bids = item.bids_set.all()
    participants = item.participants.all()
    print("167 Auctioneers:", participants, type(participants))

    if item.highest_price == 0:
        item.highest_price = item.reverse_price

    if request.method == "POST":
        amount = int(request.POST.get('amount'))
        if amount > item.highest_price:
            item.highest_price = amount
            item.save()
            bid = Bids.objects.create(
                bidder=request.user,
                item=item,
                amount=int(request.POST.get('amount'))
            )
            item.participants.add(request.user)

        return redirect('item_detail', pk=item.id)

    context = {'item': item, 'images': images, 'bids': item_bids, 'participants': participants}
    return render(request, 'app_reg_login/item_details.html', context)


def item_edit(request, pk):
    item = Item.objects.get(id=pk)
    images = ImageTable.objects.all().filter(item=item)
    form = SellForm(instance=item)
    image_form = ImageForm(instance=images)

    if request.user != item.seller:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        form = SellForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_detail', pk)

    context = {'form': form, 'image_form': image_form, 'item': item, 'edit': 'edit'}
    return render(request, 'app_reg_login/sell_item.html', context)


def item_delete(request, pk):
    item = Item.objects.get(id=pk)
    images = ImageTable.objects.all()
    count = 0

    if request.method == 'POST':
        for image in images:
            if item == image.item:
                print(count)
                count += 1
                image.delete()
        return redirect('home')
    context = {'item': item}
    return render(request, 'app_reg_login/item_delete.html', context)









