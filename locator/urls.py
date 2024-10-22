from django.urls import path
from locator.views import show_locator

app_name = 'locator'

urlpatterns = [
    path('', show_locator, name='locator'),
]
