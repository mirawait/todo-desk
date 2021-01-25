from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *


def home(request):
    return HttpResponse('ToDo Home')


def task(request):
    if request.method == "POST":
        if "Add" in request.POST:
            title = request.POST["title"]
            description = request.POST["description"]
            #date_created = str(request.POST["date_created"])
            date_end = str(request.POST["date_end"])
            status = request.POST["status"]
            created_task = Task(title=title, description=description, date_end=date_end,
                                status=status)
            created_task.save()
            return redirect("/")
        if "Delete" in request.POST:
            checkedlist = request.POST.getlist('checkedbox')
            for i in range(len(checkedlist)):
                tasks = Task.objects.filter(id=int(checkedlist[i]))
                tasks.delete()
    tasks = Task.objects.all()
    return render(request, "home.html", {"tasks": tasks, "statuses": Task.STATUS_CHOICES})
