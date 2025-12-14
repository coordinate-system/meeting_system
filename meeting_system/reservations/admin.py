from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "room", "date", "start_hour", "end_hour", "status")

    list_filter = ("status", "date")
    search_fields = ("user__username", "room__name")
    readonly_fields = ("approve_time",)

    actions = ["approve_reservation", "reject_reservation"]

    def save_model(self, request, obj, form, change):
        print("Admin save reservation:", obj.id, obj.status)
        # create_reservation / update
        # super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        print("Admin delete reservation:", obj.id)
        # cancel_reservation(obj.id)
        # super().delete_model(request, obj)

    @admin.action(description="审批通过")
    def approve_reservation(self, request, queryset):
        for res in queryset:
            print("Admin approve:", res.id)
            # approve_reservation(res.id, request.user.id)

    @admin.action(description="审批驳回")
    def reject_reservation(self, request, queryset):
        for res in queryset:
            print("Admin reject:", res.id)
            # reject_reservation(res.id, request.user.id, "管理员驳回")
