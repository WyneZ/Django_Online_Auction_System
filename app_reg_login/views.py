from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from .forms import MyUserCreationForm, UserForm, SellForm, ImageForm, TransitionForm
from .models import User, Item, ImageTable, Bids, Transition, Comment, Advertisement

# for login required to enter home
from django.contrib.auth import authenticate, login, logout

from django.urls import reverse


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


def create_item_list(item_dict):
    item_list: list = []
    item_count = 1
    for item in item_dict:
        if item_count < 10 and item.due_date != "expired":
            item_count += 1
            item_list.append(item)
        elif item_count == 10:
            break
    return item_list


def create_img_list(item_list, item_dict):
    image_list: list = []
    for item in item_list:
        image_list.append(item_dict[item])
    return image_list


def create_ad_dict(all_ads, all_items, all_images, place):
    final_dict = {}
    count = 0
    for ad in all_ads:
        for item in all_items:
            if ad.item == item and count == 0 and ad.item.due_date != "expired":
                if ad.place == place:
                    print(97, item)
                    img_list = []
                    for image in all_images:
                        if image.item == ad.item:
                            if len(img_list) < 2:
                                img_list.append(image.image_url)
                                print(105, img_list)
                                img_dict = {ad.item: img_list}
                                final_dict.update(img_dict)
                            else:
                                break

                    count = 1
    return final_dict


class MyView(View):

    def get(self, request):
        latest_items = Item.objects.all()
        all_images = ImageTable.objects.all()

        # when item expired
        for item in latest_items:
            now = datetime.now()
            if item.due_date != "expired":
                due_date = datetime.strptime(item.due_date, "%Y-%m-%dT%H:%M")
                # print(42, due_date-now-timedelta(hours=6, minutes=30))

                final_date = due_date - now - timedelta(hours=6, minutes=30)
                if final_date < timedelta(minutes=1):
                    print(48, item.title)
                    item.due_date = "expired"
                    print(50, len(item.participants.all()))
                    if len(item.participants.all()) > 0:
                        item.seller.coin_amount = item.seller.coin_amount + item.sell_price
                        item.seller.save()
                    item.save()

        # delete image if user account is deleted
        for image in all_images:
            if image.item.seller is None:
                image.delete()

        ending_dict = ending_soon_items()
        ending_list = create_item_list(ending_dict)
        ending_img_list = create_img_list(ending_list, ending_dict)

        latest_dict = create_related_dict(latest_items, all_images)
        latest_list = create_item_list(latest_dict)
        latest_img_list = create_img_list(latest_list, latest_dict)

        popular_dict = popular_items()
        popular_list = create_item_list(popular_dict)
        popular_img_list = create_img_list(popular_list, popular_dict)

        all_ads = Advertisement.objects.all()
        m1 = create_ad_dict(all_ads, latest_items, all_images, "master1")
        m2 = create_ad_dict(all_ads, latest_items, all_images, "master2")
        m3 = create_ad_dict(all_ads, latest_items, all_images, "master3")
        b1 = create_ad_dict(all_ads, latest_items, all_images, "Branch1")
        b2 = create_ad_dict(all_ads, latest_items, all_images, "Branch2")


        print(118, b1)
        ad_dict = {}

        for ad in Advertisement.objects.all():
            print(111, ad.place, ad.item)
        print(110, ad_dict)
        # context = {"ending_dict": ending_dict, "latest_dict": related_dict, "popular_dict": popular_dict, "ending_list": ending_list, "ending_img_list": ending_img_list}
        context = {"ending_list": ending_list, "ending_img_list": ending_img_list,
                   "latest_list": latest_list, "latest_img_list": latest_img_list,
                   "popular_list": popular_list, "popular_img_list": popular_img_list,
                   "m1_dict": m1, "m2_dict": m2, "m3_dict": m3, "b1_dict": b1, "b2_dict": b2,}

        return render(request, 'app_reg_login/home.html', context)

    # this is for Logout button
    def post(self, request):
        logout(request)
        return redirect('login')


def ending_soon_items():
    eItem_querySet = Item.objects.all().order_by('due_date')
    image_list = ImageTable.objects.all()
    show_dict = create_related_dict(eItem_querySet, image_list)
    return show_dict


def popular_items():
    pItem_querySet = Item.objects.all().order_by('-like_count')
    image_list = ImageTable.objects.all()
    show_dict = create_related_dict(pItem_querySet, image_list)
    return show_dict


def show_categories(request):
    return render(request, 'app_reg_login/catagory.html')


def signup(request):
    # form = MyUserCreationForm()
    print(171, request.user)

    if request.method == "POST":
        print(93, "register section.")
        username = request.POST.get('name')
        email = request.POST.get('email')
        nrc_no = request.POST.get('front') + "/" + request.POST.get('middle_1') + request.POST.get(
            'middle_2') + request.POST.get('back')
        address = request.POST.get('address') + " | " + request.POST.get('city') + " | " + request.POST.get('state')
        ph_no = request.POST.get('phNo')
        password = request.POST.get('password')

        try:
            created_user = User.objects.get(user_email=email)
        except:
            print(101)
            print(f'name: {username} '
                  f'email: {email} '
                  f'nrc: {nrc_no} '
                  f'address: {address} '
                  f'ph: {ph_no} '
                  f'password: {password}')

            user = User.objects.create(
                name=str(username),
                username=username.strip(' '),
                user_email=email,
                email=email,
                nrc_no=nrc_no,
                address=address,
                phone=ph_no,
                password=password,
                user_password=password,
            )
            user.save()
            print("134 DONE REGISTRATION", user)
            login(request, user)
            return redirect('home')
        # form = MyUserCreationForm(request.POST)
        # if form.is_valid():
        #     print(74,form.data.get('username'))
        #     mutable_form = form.data.copy()
        #     mutable_form['username'] = "WyneZ"
        #
        #     print(75, mutable_form.get('username'))
        #     print("Form is valid")
        #     user = form.save()
        #     # user = mutable_form
        #     # user.username = user.name.lower()
        #     user.save()
        #     print(f'Name: UserName:{user.username}'
        #           f'Email: {user.email} '
        #           f'Phone: {user.phone} ')
        #     login(request, user)
        #     return redirect('home')
        # else:
        #     print("SignUp Form failed.")
        #     messages.error(request, 'An error occurs during signup')

    # context = {'form': form}
    return render(request, 'app_reg_login/reg_login.html')


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('home')
        else:
            return redirect('login')

    if request.method == 'POST':
        email = request.POST['login_email']
        password = request.POST['login_password']
        print(f'173, Lemail: {email} | Lpassword: {password}')
        user = None
        try:
            user = User.objects.get(user_email=email, password=password)
            print(176, user)
        except:
            print("User Not Found!!!")

        # user = authenticate(request, email=email, password=password)
        print('authenticated >>', user)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print('123 Login Error!!')
    context = {'page': page}
    return render(request, 'app_reg_login/reg_login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id=pk)
    print(186)
    user.email = user.user_email
    user.save()
    print(188, user.email)
    all_items = user.item_set.all()
    images = ImageTable.objects.all()
    transactions = Transition.objects.all()
    transactions_history = []

    for transaction in transactions:
        if transaction.buyer == user:
            transactions_history.append(transaction)

    # to get bidded history
    bidded_querySet = Item.objects.filter(participants__email=user.user_email)
    bidded_dict = create_related_dict(bidded_querySet, images)
    print(239, bidded_querySet)

    # to get win item history
    win_querySet = Item.objects.filter(winner=str(user))
    win_dict = create_related_dict(win_querySet, images)
    print(240, win_dict)

    sell_dict = create_related_dict(all_items, images)

    if request.method == 'POST':
        logout(request)
        items = Item.objects.all()
        for item in items:
            if item.winner == str(request.user):
                item.winner = "none"
                item.save()
        user.delete()
        return redirect('home')

    print(297, transactions_history[0].buying_time)
    context = {'user': user, 'sell_dict': sell_dict, 'bidded_dict': bidded_dict, 'win_dict': win_dict,
               'transactions_history': transactions_history}
    return render(request, 'app_reg_login/profile.html', context)


@login_required(login_url='login')
def updateUser(request, pk):
    # user = request.user
    # form = UserForm(instance=user)
    #
    # if request.method == "POST":
    #     form = UserForm(request.POST, request.FILES, instance=user)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('profile', user.id)
    #
    # context = {'form': form}
    # return render(request, 'app_reg_login/updateUser.html', context)

    if request.method == "POST":
        img = request.FILES.get('update_img')
        print(280, img)
        items = Item.objects.all()
        user = User.objects.get(pk=pk)
        if img is None:
            img = user.avatar
            print(290, "SET IMG")
        print(281, str(request.POST.get('user_username')).replace(' ', ''))
        if user.name is None:
            user.name = user.username
            user.save()
        print(278, user)
        print(279, str(user), str(request.user))
        for item in items:
            if item.winner == user.username:
                item.winner = str(request.POST.get('user_username')).strip(' ')
                print("Before", item.winner)
                item.save()
                print("After", item.winner)

        user.avatar = img
        user.username = str(request.POST.get('user_username')).replace(' ', '')
        user.name = request.POST.get('user_username')
        user.user_email = request.POST.get('email')
        user.email = request.POST.get('email')
        user.nrc_no = request.POST.get('nrc_no')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        user.save()
        print(302, user.name, user.username)
    return redirect('profile', request.user.id)


def sellItem(request):
    # form = SellForm()
    # items = Item.objects.all()
    #
    # if request.method == 'POST':
    #     print("145 Doing!!")
    #     form = SellForm(request.POST, request.FILES)
    #     # print(147, "Test due date", str(request.POST.get('dueDatePicker', False)))
    #
    #     if form.is_valid():
    #         print("150 Form is valid!!!!")
    #         item = form.save()
    #         item.seller = request.user
    #         item.category = str(request.POST.get("category"))
    #         item.due_date = str(request.POST.get('dueDatePicker', False))
    #         print(152, "This is due date", item.due_date)
    #         item.save()
    #
    # images = request.FILES.getlist('upload_images')
    # for image in images:
    #     image = ImageTable.objects.create(
    #         item=item,
    #         image_url=image
    #     )
    #
    #         print(193, str(request.POST.get("category")))
    #         print(194, type(request.POST.get("category")))
    #     else:
    #         print("Form is invalid!!")
    #
    #     return redirect('home')
    # context = {'form': form}

    if request.method == "POST":
        seller = request.user
        category = request.POST.get("category")
        title = request.POST.get("title")
        item_name = request.POST.get("item_name")
        description = request.POST.get("description")
        number_of_items = request.POST.get("number_of_items")
        estimated_era = request.POST.get("estimated_era")
        country_of_origin = request.POST.get("country_of_origin")
        item_condition = request.POST.get("item_condition")
        reverse_price = request.POST.get("reverse_price")
        once_up = request.POST.get("once_up")
        due_date = request.POST.get("dueDatePicker", False)
        imgs = request.FILES['sell_imgs']
        print(332, imgs)
        print(f'POST>>{seller}\n'
              f'{category}\n'
              f'{title}\n'
              f'{item_name}\n'
              f'{description}\n'
              f'{number_of_items}\n'
              f'{estimated_era}\n'
              f'{country_of_origin}\n'
              f'{item_condition}\n'
              f'{reverse_price}\n'
              f'{once_up}\n'
              f'{due_date}\n')

        item = Item.objects.create(
            seller=request.user,
            category=request.POST.get("category"),
            title=request.POST.get("title"),
            item_name=request.POST.get("item_name"),
            description=request.POST.get("description"),
            number_of_items=request.POST.get("number_of_items"),
            estimated_era=request.POST.get("estimated_era"),
            country_of_origin=request.POST.get("country_of_origin"),
            item_condition=request.POST.get("item_condition"),
            reverse_price=request.POST.get("reverse_price"),
            once_up=request.POST.get("once_up"),
            due_date=request.POST.get("dueDatePicker", False),
        )

        images = request.FILES.getlist('sell_imgs')
        for image in images:
            image = ImageTable.objects.create(
                item=item,
                image_url=image
            )
        print(368, item.reverse_price)

    return redirect('profile', request.user.id)


def item_detail(request, pk):
    item = Item.objects.get(id=pk)
    url = reverse('item_detail', kwargs={'pk': item.id})
    images = ImageTable.objects.filter(item=item)
    print(279, type(images))
    item_bids = item.bids_set.all()
    participants = item.participants.all()
    comments = item.comment_set.all()
    replies = []

    review_count = 0
    for comment in comments:
        if comment.parent_comment is not None:
            replies.append(comment)
            print(221, replies[0].item.title)
        else:
            review_count += 1
    print(218, type(comments))

    if item.sell_price == 0:
        item.sell_price = item.reverse_price

    else:
        # when winner deleted account
        related_bids_querySet = Bids.objects.filter(item=item)
        sell_price = related_bids_querySet[0].amount
        for bid in related_bids_querySet:
            if bid.amount > sell_price:
                sell_price = bid.amount

        item.sell_price = sell_price
        item.save()
        print("217 This is new sell price:", item.sell_price)

    if request.method == "POST":
        print(472, request.POST.get('o1'))
        user_count = 0
        for participant in participants:
            user_count += 1
            print(252, "uc:", user_count)
            print(253, "participants:", participants[0])

        amount = int(request.POST.get('amount'))
        once_up = item.sell_price + int(item.once_up)

        if (request.user.coin_amount >= amount) and (amount >= once_up):
            # give back coin to second winner
            if user_count > 1:
                print(260, "Before:", participants[1].coin_amount)
                participants[1].coin_amount = participants[1].coin_amount + item.sell_price
                participants[1].save()
                print((262, "After:", participants[1].coin_amount))

            request.user.coin_amount = request.user.coin_amount - amount
            request.user.save()
            item.sell_price = amount
            item.winner = str(request.user)
            item.save()
            Bids.objects.create(
                bidder=request.user,
                item=item,
                amount=int(request.POST.get('amount'))
            )
            item.participants.add(request.user)
            print("Winner:", item.winner)

        return redirect('item_detail', pk=item.id)

    related_querySet = Item.objects.filter(category=item.category)
    related_dict = create_related_dict(related_querySet, ImageTable.objects.all())
    related_list = create_item_list(related_dict)
    related_img_list = create_img_list(related_list, related_dict)

    context = {'item': item, 'images': images, 'bids': item_bids, 'participants': participants, 'comments': comments,
               'replies': replies, 'review_count': review_count, 'related_list': related_list,
               'related_img_list': related_img_list}
    return render(request, 'app_reg_login/item_details.html', context)


def item_bid_btn(request, item, btn_no):
    bid_item = Item.objects.get(id=item)
    if request.method == "POST":
        if btn_no == '1':
            if bid_item.sell_price == 0:
                bid_item.sell_price = bid_item.reverse_price + bid_item.once_up
            else:
                bid_item.sell_price += bid_item.once_up
            print(520, bid_item.sell_price)
        elif btn_no == '2':
            if bid_item.sell_price == 0:
                bid_item.sell_price = bid_item.reverse_price + (bid_item.once_up * 2)
            else:
                bid_item.sell_price += bid_item.once_up
            print(522)
        else:
            if bid_item.sell_price == 0:
                bid_item.sell_price = bid_item.reverse_price + (bid_item.once_up * 3)
            else:
                bid_item.sell_price += bid_item.once_up * 3
            print(524)
        bid_item.winner = str(request.user)
        bid_item.participants.add(request.user)
        bid_item.save()
        Bids.objects.create(
            bidder=request.user,
            item=bid_item,
            amount=bid_item.sell_price
        )
        print(530, bid_item.sell_price, bid_item.winner)
    return redirect('item_detail', item)


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


def search_item(request, page):
    image_list = ImageTable.objects.all()
    if page == "navbar":
        sItem = request.GET.get('sItem') if request.GET.get('sItem') is not None else ''
        print(342, sItem)
        sItem_querySet = Item.objects.filter(
            Q(title__icontains=sItem)
        )
        show_dict = create_related_dict(sItem_querySet, image_list)
    elif page == "Ending Soon":
        sItem = page
        show_dict = ending_soon_items()
    elif page == "Latest Post":
        sItem = page
        show_dict = create_related_dict(Item.objects.all(), image_list)
    elif page == "Popular Post":
        sItem = page
        show_dict = popular_items()
    else:
        sItem = page
        sItem_querySet = Item.objects.filter(category=sItem)
        show_dict = create_related_dict(sItem_querySet, image_list)

    context = {'sItem': sItem, 'show_dict': show_dict}
    return render(request, 'app_reg_login/search.html', context)


@login_required(login_url='login')
def like_item(request, pk, page):
    item = Item.objects.get(id=pk)
    liked_users = item.liked_users.all()
    print(248, 'early liked_users>>', liked_users)

    if request.method == "POST":
        if request.user in liked_users:
            item.liked_users.remove(request.user)
            item.like_count = item.like_count - 1
        else:
            item.liked_users.add(request.user)
            item.like_count = item.like_count + 1
        item.save()
        print(252, item.liked_users.all())

        if page == 'detail':
            return redirect('item_detail', item.id)

    return redirect('/')


@login_required(login_url='login')
def buying_coin(request):
    # form = TransitionForm
    # buyer = request.user
    # if request.method == "POST":
    #     print("Get into Transaction:")
    #     form = TransitionForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         print("TransitionForm is valid")
    #         transition = form.save()
    #         transition.buyer = buyer
    #         transition.save()
    #
    # if buyer.coin_amount == 0:
    #     buyer.coin_amount = transition.coin_amount
    #     print(285, buyer.coin_amount)
    # else:
    #     buyer.coin_amount = buyer.coin_amount + transition.coin_amount
    # request.user.save()
    #
    #         print(f'Buyer: {transition.buyer.name} '
    #               f'Coin Amount: {transition.coin_amount} '
    #               f'Invoice No: {transition.invoice_no} '
    #               f'Payment Method: {transition.payment_method} '
    #               f'Invoice Img: {transition.invoice_img}'
    #               f'Buying Time: {transition.buying_time}')
    #
    #         return redirect('home')
    #     else:
    #         messages.error(request, 'An error occurs when buying coin')
    buyer = request.user

    if request.method == "POST":
        buyer_nrc = request.POST.get('front') + "/" + request.POST.get('mid1') + request.POST.get(
            'mid2') + request.POST.get('back')
        buyer_ph = request.POST.get('buyer_ph')
        coin_amount = request.POST.get('coin_amount')
        invoice_no = request.POST.get('invoice_no')
        payment_method = request.POST.get('payment_method')
        invoice_img = request.FILES['invoice_img']
        status = "in"
        print(598)
        transaction = Transition.objects.create(
            buyer=buyer,
            buyer_nrc=buyer_nrc,
            buyer_ph=buyer_ph,
            coin_amount=coin_amount,
            invoice_no=invoice_no,
            payment_method=payment_method,
            invoice_img=invoice_img,
            status=status,
        )
        transaction.save()
        if buyer.coin_amount == 0:
            buyer.coin_amount = int(transaction.coin_amount)
            print(285, buyer.coin_amount)
        else:
            buyer.coin_amount = buyer.coin_amount + int(transaction.coin_amount)
        request.user.save()
        print(610, transaction)
        # print(f'{buyer.username}'
        #       f'{buyer_nrc}'
        #       f'{buyer_ph}'
        #       f'{coin_amount}'
        #       f'{invoice_no}'
        #       f'{payment_method}'
        #       f'{invoice_img}'
        #       f'{status}'
        #       )

    return render(request, 'app_reg_login/buying_coin.html')


def transfer_money(request):
    transfer_user = request.user

    if request.method == "POST":
        buyer_nrc = request.POST.get('Tfront') + "/" + request.POST.get('Tmid1') + request.POST.get(
            'Tmid2') + request.POST.get('Tback')
        buyer_ph = request.POST.get('transfer_ph')
        coin_amount = request.POST.get('Tcoin_amount')
        payment_method = request.POST.get('Tpayment_method')
        status = "out"
        if transfer_user.coin_amount >= int(coin_amount) and transfer_user.coin_amount > 0:
            transaction = Transition.objects.create(
                buyer=transfer_user,
                buyer_nrc=buyer_nrc,
                buyer_ph=buyer_ph,
                coin_amount=coin_amount,
                payment_method=payment_method,
                status=status,
            )
            transfer_user.coin_amount = transfer_user.coin_amount - int(transaction.coin_amount)
            request.user.save()

    return render(request, 'app_reg_login/buying_coin.html')


def advertising_item(request, pk, place):
    item = Item.objects.get(id=pk)
    if request.method == "POST":
        advertisement = Advertisement.objects.create(
            user=request.user,
            item=item,
        )
        if place == "master" and request.user.coin_amount >= 20:
            master = request.POST.get("ad_master")
            advertisement.place = master
            advertisement.ad_coin = 20
            request.user.coin_amount = request.user.coin_amount - 20
            request.user.save()
            print(664, master)
            advertisement.save()
            return redirect('/')

        elif place == "branch" and request.user.coin_amount >= 10:
            branch = request.POST.get("ad_branch")
            advertisement.place = branch
            advertisement.ad_coin = 10
            request.user.coin_amount = request.user.coin_amount - 10
            request.user.save()
            print(667, branch)
            advertisement.save()
            return redirect('/')
    context = {'item': item}
    return render(request, 'app_reg_login/advertising.html', context)


def comment_section(request, pk):
    item = Item.objects.get(id=pk)
    print(365, "This is comment section")
    if request.method == "POST":
        Comment.objects.create(
            user=request.user,
            item=item,
            text=str(request.POST.get('comment_text'))
        )
        print(372, "Commented Successfully!!!!!!")
        print(375, request.POST.get("comment_text"))
        return redirect('item_detail', pk)
    return render(request, 'app_reg_login/item_details_old.html')


def reply_section(request, comment_id):
    parent_comment = Comment.objects.get(id=comment_id)
    item = parent_comment.item
    if request.method == "POST":
        Comment.objects.create(
            user=request.user,
            item=item,
            text=str(request.POST.get('reply_text')),
            parent_comment=parent_comment
        )
        return redirect('item_detail', item.id)

    return render(request, 'app_reg_login/item_details_old.html')

# OTP password
# texl rorl pfog xhwe
