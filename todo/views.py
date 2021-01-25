from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TaskSerializer


def home(request):
    return HttpResponse('ToDo Home')


def task(request):
    if request.method == "POST":
        if "Add" in request.POST:
            title = request.POST["title"]
            description = request.POST["description"]
            # date_created = str(request.POST["date_created"])
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


class TaskView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response({"tasks": serializer.data})

    def post(self, request):
        task_api = request.data.get('task')
        serializer = TaskSerializer(data=task_api)
        if (serializer.is_valid(raise_exception=True)):
            task_saved = serializer.save()
        return Response({"success": "Task '{}' created successfully".format(task_saved.title)})

    def put(self, request, pk):
        print(f"pk={pk}")
        saved_task = get_object_or_404(Task.objects.all(), pk=pk)
        data = request.data.get('task')
        serializer = TaskSerializer(instance=saved_task, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            updated_task = serializer.save()

        return Response({"success": "Task '{}' was updated".format(updated_task.title)})
