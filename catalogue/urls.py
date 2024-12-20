from django.urls import path
from catalogue.views import *

app_name = 'catalogue'

urlpatterns = [
    path('', show_products, name='show_products'),
    path('add/', add_product_entry, name='add_product_entry'),
    path('edit/<uuid:product_id>/', edit_product, name='edit_product'),
    path('delete/<uuid:product_id>/', delete_product, name='delete_product'),
    path('add_review/<uuid:product_id>/', add_review, name='add_review'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),
    path('filter_ajax/', filter_products_ajax, name='filter_products_ajax'),
    path('get_product/', get_product, name='get_product'),
    path('get_review/', get_review, name='get_reviews'),
    path('review_flutter/<uuid:product_id>/', review_flutter, name='review_flutter'),
    path('delete_review_flutter/<int:review_id>/', delete_review_flutter, name='delete_review_flutter'),
    path('add_product_flutter/', add_product_flutter, name='add_product_flutter'),
    path('delete_product_flutter/<uuid:product_id>/', delete_product_flutter, name='delete_product_flutter'),
    path('edit_product_flutter/<uuid:product_id>/', edit_product_flutter, name='edit_product_flutter'),
    path('get_product_flutter/<uuid:product_id>/', get_product_flutter, name='get_product_flutter'),
    path('filter_products_flutter/', filter_products_flutter, name='filter_products_flutter'),

]