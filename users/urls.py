from django.urls import path
from .views import create_user, login_user, forgot_password, reset_password

urlpatterns = [
    path('signup/', create_user, name='create_user'),
    path('login/', login_user, name='login_user'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/', reset_password, name='reset_password'),
]
