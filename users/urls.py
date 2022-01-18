from django.urls import path, include
from users.views import dashboard

urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('', dashboard, name="dashboard"),
    #path('dashboard/', dashboard, name="dashboard"),
]