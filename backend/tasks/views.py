from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import TaskForm
from .models import Task

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect(reverse("tasks:task_list"))
    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", {"form": form, })

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def task_detail(request, pk):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse("tasks:task_list"))
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect(reverse("tasks:task_list"))