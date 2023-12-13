from django.urls import path
from .views import *

urlpatterns = [
    path('auth/register/', register, name='register'),
    path('auth/signin/', sign_in, name='signin'),
    path('auth/validate_token/', validate_token, name='validate_token'),
]