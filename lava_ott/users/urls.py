from django.urls import path
from .views import *


urlpatterns = [
    path('login/', AdminLoginView.as_view()),
    path('status/', StatusView.as_view()),
    path('logout/', AdminLogoutView.as_view()),

    path('otp-send/', OTPSendView.as_view()),
    path('otp-validate/', OTPVerifyView.as_view()),

    path('list/', UserListView.as_view()),

    # Mobile App
    path('app/registration/', UserRegistrationView.as_view()),
    path('app/status/', UserStatusAppView.as_view()),
    path('app/profile/', UserProfileView.as_view()),
]
