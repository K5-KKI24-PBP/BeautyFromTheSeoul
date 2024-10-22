from django.urls import path
from catalogue.views import show_products

app_name = 'catalogue'

urlpatterns = [
    path('', show_products, name='show_products'),   
]