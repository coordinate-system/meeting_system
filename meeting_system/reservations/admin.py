from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone
from django.utils.html import format_html
from .models import Reservation


# 1. 定义自定义表单，用于处理验证逻辑
class ReservationAdminForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        # 获取表单数据
        room = cleaned_data.get("room")
        date = cleaned_data.get("date")
        start_hour = cleaned_data.get("start_hour")
        end_hour = cleaned_data.get("end_hour")
        status = cleaned_data.get("status")

        # 如果基本数据不全，直接返回（由Django默认字段验证处理）
        if not (room and date and start_hour is not None and end_hour is not None):
            return cleaned_data

        # 逻辑检查：结束时间不能早于开始时间
        if start_hour >= end_hour:
            raise ValidationError("结束时间必须晚于开始时间")

        # 冲突检查逻辑
        # 排除状态为 CANCELED 和 REJECTED 的记录
        # 排除当前正在编辑的记录 (self.instance.id)，防止修改时报错
        conflict_queryset = (
            Reservation.objects.filter(
                room=room, date=date, status__in=["PENDING", "APPROVED", "USED"]
            )
            .exclude(id=self.instance.id)  # 关键：排除自己，支持编辑操作
            .filter(
                # 冲突条件：(现有开始 < 新结束) AND (现有结束 > 新开始)
                start_hour__lt=end_hour,
                end_hour__gt=start_hour,
            )
        )

        if conflict_queryset.exists():
            conflict_res = conflict_queryset.first()
            raise ValidationError(
                f"该时段与已有预约冲突！冲突预约人：{conflict_res.user.username}，"
                f"时间：{conflict_res.start_hour}:00 - {conflict_res.end_hour}:00"
            )

        return cleaned_data


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    # 2. 挂载自定义表单
    form = ReservationAdminForm

    list_display = (
        "id",
        "user",
        "room",
        "date",
        "display_time_range",
        "topic",
        "status_colored",
        "approve_time",
    )
    list_filter = ("status", "date", "room")
    search_fields = ("user__username", "topic")

    fieldsets = (
        (
            "基本信息",
            {"fields": ("user", "room", "date", ("start_hour", "end_hour"), "topic")},
        ),
        ("审批状态", {"fields": ("status", "reject_reason", "approve_time")}),
    )

    readonly_fields = ("approve_time",)

    def display_time_range(self, obj):
        return f"{obj.start_hour}:00 - {obj.end_hour}:00"

    display_time_range.short_description = "预约时间段"

    from django.utils.html import format_html

    def status_colored(self, obj):
        colors = {
            "PENDING": "orange",
            "APPROVED": "green",
            "REJECTED": "red",
            "CANCELED": "gray",
            "USED": "blue",
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, "black"),
            obj.get_status_display(),
        )

    status_colored.short_description = "状态"

    # 审批相关的 Actions 保持不变...
    @admin.action(description="审批通过所选预约")
    def approve_reservations(self, request, queryset):
        rows_updated = queryset.exclude(status__in=["CANCELED", "REJECTED"]).update(
            status="APPROVED", approve_time=timezone.now()
        )
        self.message_user(request, f"{rows_updated} 个预约已通过审批。")

    @admin.action(description="驳回所选预约")
    def reject_reservations(self, request, queryset):
        rows_updated = queryset.exclude(status="CANCELED").update(
            status="REJECTED",
            reject_reason="管理员后台批量驳回",
            approve_time=timezone.now(),
        )
        self.message_user(request, f"{rows_updated} 个预约已驳回。")

    actions = [approve_reservations, reject_reservations]

    def save_model(self, request, obj, form, change):
        if change:
            if obj.status in ["APPROVED", "REJECTED"] and not obj.approve_time:
                obj.approve_time = timezone.now()
        super().save_model(request, obj, form, change)
