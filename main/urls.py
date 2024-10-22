from django.urls import path
from main.views import show_main, create_ad

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create_ad/', create_ad, name='create_ad'),
]
