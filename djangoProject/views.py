from django.http import HttpResponse


def home(request):
    return HttpResponse('<a href="http://localhost:8000/page1">Page 1</a>')


def page1(request):
    return HttpResponse('This is page 1. <a href="http://localhost:8000">Back</a> to home page')
