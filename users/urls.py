from django.urls import path, include
from users.views import *

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', login, name="login"),
    path('password_reset/', login, name="password_reset"),
    path('', dashboard, name="dashboard"),
]