from django.contrib import admin
from django.urls import path,include
from user_management.views import *
from .views import GoogleLogin

from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
)

urlpatterns = [
    path('register/',UserRegister.as_view(),name='register'),
    path('login/',UserLogin.as_view(),name='Login'),
    path('profile/',UserProfile.as_view(),name='Profile'),
    path('logout/',UserLogout.as_view(),name='logout'),

    path('changepassword/',ChangePassword.as_view(),name='Change- password'),
    path('sendresetpasswordemail/',SendResetPasswordEmail.as_view(),name='send-email'),
    path('resetpassword/<str:uid>/<str:token>/',ResetPassword.as_view(),name='reset-password'),

    path('token/', TokenObtainSlidingView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),

    path('auth/social/login/google/', GoogleLogin.as_view(), name='google_login'),
    
    path('login_otp/',FirstLogin.as_view(),name='otp_login'),
    path('verify_otp/',VerifyOTP.as_view(),name='Verify_otp')
]


