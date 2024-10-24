from django.urls import path
from favorites.views import show_favorites, add_favorites, remove_favorites

app_name = 'favorites'

urlpatterns = [
    path('add/<int:product_id>/', add_favorites, name="add_favorites"),
    path('remove/<int:product_id>/',remove_favorites, name="remove_favorites"),
    path('', show_favorites, name='favorites'),
]