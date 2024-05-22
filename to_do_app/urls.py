from django.urls import path

from to_do_app.views import home, register, login_view, logout_view, add_task, edit_task, delete_task, toggle_task, \
    tag_list, add_tag, edit_tag, delete_tag

app_name = "to_do_app"

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('task/add/', add_task, name='add_task'),
    path('task/<int:pk>/edit/', edit_task, name='edit_task'),
    path('task/<int:pk>/delete/', delete_task, name='delete_task'),
    path('task/<int:pk>/toggle/', toggle_task, name='toggle_task'),
    path('tags/', tag_list, name='tag_list'),
    path('tags/add/', add_tag, name='add_tag'),
    path('tags/<int:pk>/edit/', edit_tag, name='edit_tag'),
    path('tags/<int:pk>/delete/', delete_tag, name='delete_tag'),
]
