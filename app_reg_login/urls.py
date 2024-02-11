from django.urls import path
from app_reg_login.views import MyView
from . import views


urlpatterns = [
    path('', MyView.as_view(), name='home'),

    # user management
    path('register/', views.signup, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('update/', views.updateUser, name='update'),
    path('profile/<str:pk>', views.profile, name='profile'),

    # auction Listing & bidding
    path('sell/', views.sellItem, name='sell'),
    path('item_detail/<str:pk>', views.item_detail, name="item_detail"),
    path('item_edit/<str:pk>', views.item_edit, name="item_edit"),
    path('item_delete/<str:pk>', views.item_delete, name="item_delete"),

    # rating
    path('like_item/<str:pk>', views.like_item, name="like_item"),

    # search
    path('search_item/', views.search_item, name="search_item"),

    # buying coin
    path('buying_coin/', views.buying_coin, name="buying_coin"),


]


#
# Implementing SMS OTP (One-Time Password) authentication in Django involves using a third-party SMS service
# to send OTP codes to users' mobile numbers. Here's a step-by-step guide on how to add SMS OTP authentication to your Django project:
#
# 1. Choose an SMS Service Provider:
#    Select an SMS service provider that suits your needs. Some popular choices include Twilio, Nexmo (now Vonage), or Plivo. Sign up for an account with your chosen provider and obtain the necessary API credentials (account SID, token, etc.).
#
# 2. Install Required Packages:
#    You will need to install a package to send SMS messages through the SMS service provider. For example, if you choose Twilio, you can use the `twilio` package. Install it using pip:
#
#    ```
#    pip install twilio
#    ```
#
# 3. Configure SMS Service Provider:
#    In your Django project's settings, configure the SMS service provider by adding the necessary credentials. For example, for Twilio:
#
#    ```python
#    # settings.py
#    TWILIO_ACCOUNT_SID = 'your_twilio_account_sid'
#    TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'
#    TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'
#    ```
#
# 4. Generate and Send OTP:
#    Create a function to generate and send OTP codes to users' mobile numbers. You can use the `twilio` package to send SMS messages. Here's an example of how to send an OTP:
#
#    ```python
#    from twilio.rest import Client
#    from django.conf import settings
#
#    def send_otp(phone_number, otp_code):
#        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#        message = client.messages.create(
#            body=f'Your OTP code is: {otp_code}',
#            from_=settings.TWILIO_PHONE_NUMBER,
#            to=phone_number
#        )
#    ```
#
# 5. Create Views and Templates:
#    Create Django views to handle OTP verification and templates for OTP-related pages. For example, you can have views for sending OTP, verifying OTP, and displaying the OTP form.
#
# 6. Generate and Verify OTP:
#    In your Django views, generate random OTP codes when users request them and then verify the OTP entered by the user. You can use Django's built-in forms for this purpose.
#
# 7. Store and Check OTP Codes:
#    Store OTP codes in your database along with the user's phone number and a timestamp for expiration. When a user submits an OTP, compare it with the stored OTP and check if it's still valid (not expired).
#
# 8. Handle Login and Authentication:
#    After a user successfully verifies their OTP, you can log them in using Django's authentication system. You can use Django's `login()` function to achieve this.
#
# 9. Add Security Measures:
#    Ensure that you implement security measures to protect against brute-force attacks, such as rate limiting login attempts and limiting the number of OTP code validation attempts.
#
# 10. Test Your Implementation:
#     Thoroughly test your SMS OTP authentication system to make sure it works as expected.
#
# Remember that this is just a basic outline, and you can further customize the implementation based on your specific requirements and the chosen SMS service provider. Additionally, you should consider handling cases like account recovery and password reset as part of a complete authentication system.
#
#
