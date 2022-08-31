from django.urls import path 
from .views import receipts_list_and_create

urlpatterns = [
    path('receipts/',receipts_list_and_create,name='receipts'),
]