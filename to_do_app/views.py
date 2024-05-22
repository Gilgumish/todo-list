from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Case, When
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from to_do_app.forms import CustomUserCreationForm, TaskForm, TagForm
from to_do_app.models import Task, Tag


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("to_do_app:home")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
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
    sort_by = request.GET.get("sort_by", "created_at")
    if sort_by == "status":
        tasks = (
            Task.objects.filter(user=request.user)
            .annotate(
                status_order=Case(
                    When(is_done=True, then=0),
                    When(is_done=False, then=1),
                )
            )
            .order_by("status_order", "-created_at")
        )
    else:
        tasks = Task.objects.filter(user=request.user).order_by(sort_by)
    now = timezone.now()
    return render(
        request, "to-do-app/home.html", {"tasks": tasks, "now": now, "sort_by": sort_by}
    )


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
    return render(request, "to-do-app/task_form.html", {"form": form})


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
    return render(request, "to-do-app/task_form.html", {"form": form})


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("to_do_app:home")
    return render(request, "to-do-app/task_confirm_delete.html", {"task": task})


@login_required
def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_done = not task.is_done
    task.save()
    return redirect("to_do_app:home")


@login_required
def tag_list(request):
    tags = Tag.objects.all().order_by("name")
    return render(request, "to-do-app/tag_list.html", {"tags": tags})


@login_required
def add_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("to_do_app:tag_list")
    else:
        form = TagForm()
    return render(request, "to-do-app/tag_form.html", {"form": form})


@login_required
def edit_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect("to_do_app:tag_list")
    else:
        form = TagForm(instance=tag)
    return render(request, "to-do-app/tag_form.html", {"form": form})


@login_required
def delete_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        tag.delete()
        return redirect("to_do_app:tag_list")
    return render(request, "to-do-app/tag_confirm_delete.html", {"tag": tag})
