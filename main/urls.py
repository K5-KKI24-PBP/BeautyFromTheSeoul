from django.urls import path
from main.views import show_main, create_ad, delete_ad, edit_ad

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create_ad/', create_ad, name='create_ad'),
    path('delete/<uuid:id>', delete_ad, name='delete_ad'),
    path('edit-ad/<uuid:id>', edit_ad, name='edit_ad'),
]
