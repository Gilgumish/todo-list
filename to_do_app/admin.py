from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Task, Tag
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username', 'email', 'is_staff', 'is_active']


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_done', 'created_at', 'deadline')
    list_filter = ('is_done', 'created_at', 'deadline')
    search_fields = ('title', 'content', 'user__username')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Tag, TagAdmin)
