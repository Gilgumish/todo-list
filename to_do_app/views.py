from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from to_do_app.forms import CustomUserCreationForm, TaskForm
from to_do_app.models import Task


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("to_do_app:home")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("to_do_app:home")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("to_do_app:home")


@login_required
def home(request):
    tasks = Task.objects.filter(user=request.user).order_by('deadline')
    now = timezone.now()
    return render(request, "to-do-app/home.html", {'tasks': tasks, 'now': now})


@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            form.save_m2m()
            return redirect("to_do_app:home")
    else:
        form = TaskForm()
    return render(request, "to-do-app/task_form.html", {'form': form})


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("to_do_app:home")
    else:
        form = TaskForm(instance=task)
    return render(request, "to-do-app/task_form.html", {'form': form})


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("to_do_app:home")
    return render(request, 'to-do-app/task_confirm_delete.html', {'task': task})


@login_required
def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_done = not task.is_done
    task.save()
    return redirect("to_do_app:home")


