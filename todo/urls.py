from . import views
from django.urls import path

appname = 'todo'

urlpatterns = [
    path('', views.TaskView.as_view()),
    path('<int:pk>', views.TaskView.as_view()),
]
