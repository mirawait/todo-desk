from . import views
from django.urls import path, include
from .views import RegistrationAPIView, LoginAPIView

app_name = 'users'

urlpatterns = [
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/',LoginAPIView.as_view())
]
