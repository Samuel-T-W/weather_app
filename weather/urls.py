from django.urls import path
from .views import index, delete_city

urlpatterns = [
    path('', index, name='home'),
    path('delete/<city_name>/', delete_city, name='delete_city'),

]
