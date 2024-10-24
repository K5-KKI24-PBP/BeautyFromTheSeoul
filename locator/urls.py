from django.urls import path
from locator.views import show_locator, create_location_entry

app_name = 'locator'

urlpatterns = [
    path('', show_locator, name='locator'),
    path('create/', create_location_entry, name='location_entry'),
]
