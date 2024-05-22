from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import AnonymousUser

from to_do_app.forms import CustomUserCreationForm
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


def home(request):
    if not request.user.is_authenticated:
        return redirect('to_do_app:login')

    tasks = Task.objects.filter(user=request.user).order_by('-deadline')
    return render(request, "to-do-app/home.html", {'tasks': tasks})
