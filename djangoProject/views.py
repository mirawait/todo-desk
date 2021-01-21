import django.http as http
import django.shortcuts as sc


def home(request):
    return sc.render(request, 'djangoProject/index.html')


def page1(request):
    return http.HttpResponse('This is page 1. <a href="http://localhost:8000">Back</a> to home page')
