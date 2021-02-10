from . import views
from django.urls import path, include
from .views import RegistrationAPIView, LoginAPIView

app_name = 'users'

urlpatterns = [
    path('users/', include('dj_rest_auth.urls')),
    path('users/registration/', include('dj_rest_auth.registration.urls')),
]
