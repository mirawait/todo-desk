from . import views
from django.urls import path

app_name = 'todo'

urlpatterns = [
    path('', views.TaskView.as_view()),
    path('<slug:slug>/', views.TaskView.as_view()),
]
