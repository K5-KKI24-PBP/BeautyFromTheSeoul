from django.urls import path
from favorites.views import show_favorites

app_name = 'favorites'

urlpatterns = [
    path('', show_favorites, name='favorites'),
]