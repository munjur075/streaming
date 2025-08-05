from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin_login/', AdminLoginView.as_view(), name='admin_login'),

    path('verify_email/', VerifyEmailView.as_view(), name='verify_email'),
    path('send_otp/', SendOtpView.as_view(), name='send_otp'),

    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),

    path('user_profile/', UserProfileView.as_view(), name='user_profile'),
]
