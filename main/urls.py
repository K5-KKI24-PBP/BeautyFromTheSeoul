from django.urls import path
from main.views import show_main, create_ad, delete_ad, edit_ad, approve_ad, get_ads_flutter, approve_ad_flutter, delete_ad_flutter, submit_ad_flutter, edit_ad_flutter

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create_ad/', create_ad, name='create_ad'),
    path('delete/<uuid:id>', delete_ad, name='delete_ad'),
    path('edit-ad/<uuid:id>', edit_ad, name='edit_ad'),
    path('approve-ad/<uuid:id>', approve_ad, name='approve_ad'),
    path("ads/", get_ads_flutter, name="get_ads_flutter"),
    path("ads/approve/<uuid:id>/", approve_ad_flutter, name="approve_ad_flutter"),
    path("ads/delete/<uuid:id>/", delete_ad_flutter, name="delete_ad_flutter"),
    path("ads/submit/", submit_ad_flutter, name="submit_ad_flutter"),
    path("ads/edit-ad/<uuid:id>/", edit_ad_flutter, name="edit_ad_flutter"),
]
