from django.urls import path
from favorites.views import show_favorites, add_favorites, remove_favorites, get_favorites, add_favorites_flutter

app_name = 'favorites'

urlpatterns = [
    path('add/<uuid:product_id>/', add_favorites, name="add_favorites"),
    path('remove/<uuid:product_id>/',remove_favorites, name="remove_favorites"),
    path('', show_favorites, name='favorites'),
    path('get_favorites/', get_favorites, name='get_favorites'),
    path('add_favorites_flutter/', add_favorites_flutter, name="add_favorites_flutter"),
]
