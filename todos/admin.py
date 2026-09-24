from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Todo, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "user",
        "status",
        "priority",
        "due_date",
        "created_at",
    )
    list_filter = ("status", "priority")
    search_fields = ("title", "description", "user__username", "user__email")
    ordering = ("-created_at",)
