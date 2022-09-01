from django.urls import path 
from .views import *

urlpatterns = [
    path('dashboard/staff',staff_list_and_create,name='staff'),
]