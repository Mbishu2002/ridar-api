from django.urls import path
from .views import create_user, login_user

urlpatterns = [
    path('create-user/', create_user, name='create-user'),
    path('login/', login_user, name='login'),
]
