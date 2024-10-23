from django.urls import path
from catalogue.views import show_products, add_product, edit_product

app_name = 'catalogue'

urlpatterns = [
    path('', show_products, name='show_products'),
    path('add/', add_product, name='add_product'),
    path('edit/', edit_product, name='edit_product'),
]