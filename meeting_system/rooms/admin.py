from django.contrib import admin
from .models import MeetingRoom


@admin.register(MeetingRoom)
class MeetingRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "room_no", "capacity", "usage", "is_available")
    list_filter = ("is_available",)
    search_fields = ("name", "room_no")
    list_editable = ("is_available",)

    def save_model(self, request, obj, form, change):
        print("Admin save room:", obj.name)
        # create_room / update_room
        # super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        print("Admin delete room:", obj.id)
        # delete_room(obj.id)
        # super().delete_model(request, obj)
