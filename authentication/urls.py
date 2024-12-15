from django.urls import path
from authentication.views import *
app_name = 'authentication'

urlpatterns= [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('get-user/', get_user, name='get_user'),
    path('login-flutter/', login_flutter, name='login_flutter'),
    path('logout-flutter/', logout_flutter, name='logout_flutter'),
    path('register-flutter/', register_flutter, name='register_flutter'),
    path('get-user-profile/', get_user_profile, name='get_user_flutter'),
]