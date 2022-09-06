from django.urls import path 
from .views import receipts_list_and_create

urlpatterns = [
    path('receipts/',receipts_list_and_create,name='receipts'),
    path('fees/',fees_catalogue_list_and_create,name='fees_catalogue'),
]