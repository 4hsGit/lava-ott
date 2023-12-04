from django.urls import path
from .views import *


urlpatterns = [
    path('login/', AdminLoginView.as_view()),
    path('status/', StatusView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('otp-send/', OTPSendView.as_view()),
    path('otp-validate/', OTPVerifyView.as_view()),

    path('registration/', UserRegistrationView.as_view()),
    path('list/', UserListView.as_view()),
    path('profile/', UserProfileView.as_view()),
]
