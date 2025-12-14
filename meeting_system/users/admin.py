from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    search_fields = ("user__username",)

    def save_model(self, request, obj, form, change):
        print("Admin save user:", obj.user.username)
        # super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        print("Admin delete user:", obj.user.username)
        # super().delete_model(request, obj)
