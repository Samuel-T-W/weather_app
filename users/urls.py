from django.urls import path, include
from users.views import *

urlpatterns = [
    path('register/', register, name="register"),
    path('login/redirect/', login_redirect, name="login_redirect"),
    path('logout/redirect/', logout_redirect, name="logout_redirect"),
    # path('password_reset/', login, name="password_reset"),
    path('', dashboard, name="dashboard"),
]