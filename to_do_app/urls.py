from django.contrib import admin
from django.urls import path

from to_do_app.views import home, register, login_view, logout_view

app_name = "to_do_app"

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

]
