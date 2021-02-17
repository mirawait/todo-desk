from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils.text import slugify

from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated

from todo import numbersAPI
from todo import weatherAPI

def task(request):
    if request.method == "POST":
        if "Add" in request.POST:
            title = request.POST["title"]
            description = request.POST["description"]
            # date_created = str(request.POST["date_created"])
            date_end = str(request.POST["date_end"])
            status = request.POST["status"]
            author = request.POST["author"]
            created_task = Task(title=title, description=description, date_end=date_end,
                                status=status, author=author)
            created_task.save()
            return redirect("/")
        if "Delete" in request.POST:
            checkedlist = request.POST.getlist('checkedbox')
            for i in range(len(checkedlist)):
                tasks = Task.objects.filter(id=int(checkedlist[i]))
                tasks.delete()
    tasks = Task.objects.all()
    return render(request, "home.html", {"tasks": tasks, "statuses": Task.STATUS_CHOICES})


class TaskView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, slug=None):
        if slug is None:
            tasks = Task.objects.all()
            serializer = TaskSerializer(tasks, many=True)
            for item in serializer.data:
                date = datetime.strptime(item.get('date_created'), "%Y-%m-%dT%H:%M:%S.%f%z")
                item['fact'] = numbersAPI.get_fact(date.month, date.day)
                item['weather'] = weatherAPI.get_weather('Tomsk')
            return Response({"tasks": serializer.data})
        else:
            task = get_object_or_404(Task.objects.all(), slug=slug)
            serializer = TaskSerializer(task, many=False)
            item = serializer.data
            date = datetime.strptime(item.get('date_created'), "%Y-%m-%dT%H:%M:%S.%f%z")
            item['fact'] = numbersAPI.get_fact(date.month, date.day)
            item['weather'] = weatherAPI.get_weather('Tomsk')
            return Response({"tasks": item})

    def post(self, request):
        task_api = request.data.get('task')
        token_user = request.user
        task_api['author'] = token_user.username
        task_api['slug'] = slugify(task_api['title'])
        serializer = TaskSerializer(data=task_api)
        if serializer.is_valid(raise_exception=True):
            task_saved = serializer.save()
        return Response({"success": "Task '{}' created successfully".format(task_saved.title)})

    def put(self, request, slug):
        saved_task = get_object_or_404(Task.objects.all(), slug=slug)
        token_user = request.user
        if saved_task.author == token_user.username or token_user.is_staff:
            data = request.data.get('task')
            serializer = TaskSerializer(instance=saved_task, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                updated_task = serializer.save()
            return Response({"success": "Task '{}' was updated".format(updated_task.title)})

        else:
            return Response({"error": "You don't have permission"})
