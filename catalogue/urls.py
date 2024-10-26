from django.urls import path
# from catalogue.views import show_products, add_product, edit_product
from .views import *

app_name = 'catalogue'

urlpatterns = [
    path('', show_products, name='show_products'),
    path('add/', add_product_entry, name='add_product'),
    path('edit/', edit_product, name='edit_product'),
    path('delete/<uuid:product_id>/', delete_product, name='delete_product'),
    path('get_product', get_product, name='get_product'),
    path('add_review/<uuid:product_id>/', add_review, name='add_review'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),
    path('filter/', filter_products, name='filter_products'),
]