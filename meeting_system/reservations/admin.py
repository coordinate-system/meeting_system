from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.html import format_html
from datetime import datetime, timedelta

from .models import Reservation


# ===============================
# 表单校验（管理员 & 用户共用规则）
# ===============================
class ReservationAdminForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        room = cleaned_data.get("room")
        date = cleaned_data.get("date")
        start = cleaned_data.get("start_hour")
        end = cleaned_data.get("end_hour")
        status = cleaned_data.get("status")
        reject_reason = cleaned_data.get("reject_reason")

        if not all([room, date, start is not None, end is not None]):
            return cleaned_data

        today = timezone.localdate()
        now = timezone.localtime()

        # ---- 时间合法性 ----
        if start < 0 or end > 24:
            raise ValidationError("时间必须在 0-24 点之间")

        if start >= end:
            raise ValidationError("结束时间必须晚于开始时间")

        if date < today:
            raise ValidationError("预约日期不能早于今天")

        if date == today and start < now.hour:
            raise ValidationError("当天预约开始时间不能早于当前时间")

        # ---- 会议室状态 ----
        if not room.is_available:
            raise ValidationError("该会议室当前不可预约")

        # ---- USED / APPROVED 禁止改时间 ----
        if self.instance.pk:
            old = Reservation.objects.get(pk=self.instance.pk)
            if old.status in ["APPROVED", "USED"]:
                if old.start_hour != start or old.end_hour != end or old.date != date:
                    raise ValidationError("已审批或已使用的预约禁止修改时间")

        # ---- 时间冲突检查 ----
        conflict_qs = (
            Reservation.objects.filter(
                room=room,
                date=date,
                status__in=["PENDING", "APPROVED", "USED"],
            )
            .exclude(id=self.instance.id)
            .filter(start_hour__lt=end, end_hour__gt=start)
        )

        if conflict_qs.exists():
            c = conflict_qs.first()
            raise ValidationError(
                f"时间冲突：{c.user.username} {c.start_hour}:00-{c.end_hour}:00"
            )

        # ================== 状态流转校验 ==================
        if self.instance.pk:
            old_status = self.instance.status
            allowed = {
                "PENDING": ["APPROVED", "REJECTED", "CANCELED"],
                "APPROVED": ["USED", "CANCELED"],
                "REJECTED": [],
                "CANCELED": [],
                "USED": [],
            }

            if status != old_status and status not in allowed.get(old_status, []):
                raise ValidationError(f"非法状态流转：{old_status} → {status}")

            # ---- 驳回理由规则（编辑）----
            if status == "REJECTED":
                if not reject_reason:
                    raise ValidationError("驳回预约必须填写驳回理由")
            else:
                # 非 REJECTED 状态，自动清空驳回理由
                cleaned_data["reject_reason"] = ""

            # ---- USED 时间限制 ----
            if status == "USED":
                start_dt = timezone.make_aware(
                    datetime.combine(date, datetime.min.time())
                ) + timedelta(hours=start)

                if abs((now - start_dt).total_seconds()) > 3600:
                    raise ValidationError("不在允许确认使用的时间范围内")

        # ================== 新建预约校验 ==================
        if not self.instance.pk:
            if status not in ["PENDING", "APPROVED"]:
                raise ValidationError(
                    "管理员创建预约时，状态只能是「审核中」或「已通过」"
                )

            if reject_reason:
                raise ValidationError("创建预约时不能填写驳回理由")

            if status == "APPROVED" and date < today:
                raise ValidationError("不能为已过期的时间创建“已通过”的预约")

        return cleaned_data


# ===============================
# Admin 配置
# ===============================
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    form = ReservationAdminForm

    list_display = (
        "id",
        "user",
        "room",
        "date",
        "time_range",
        "topic",
        "status_colored",
        "approve_time",
    )

    list_filter = ("status", "date", "room")
    search_fields = ("user__username", "topic")

    fieldsets = (
        (
            "预约信息",
            {"fields": ("user", "room", "date", ("start_hour", "end_hour"), "topic")},
        ),
        (
            "审批信息",
            {"fields": ("status", "reject_reason", "approve_time")},
        ),
    )

    readonly_fields = ("approve_time",)

    # ---- 显示辅助 ----
    def time_range(self, obj):
        return f"{obj.start_hour}:00 - {obj.end_hour}:00"

    time_range.short_description = "时间段"

    def status_colored(self, obj):
        colors = {
            "PENDING": "orange",
            "APPROVED": "green",
            "REJECTED": "red",
            "CANCELED": "gray",
            "USED": "blue",
        }
        return format_html(
            '<b style="color:{}">{}</b>',
            colors.get(obj.status, "black"),
            obj.get_status_display(),
        )

    status_colored.short_description = "状态"

    # ===============================
    # Actions（管理员独有能力）
    # ===============================
    @admin.action(description="审批通过")
    def approve_reservations(self, request, queryset):
        now = timezone.now()
        success = 0

        for r in queryset:
            if r.status != "PENDING":
                continue

            # 过期不能审批
            if r.date < timezone.localdate():
                continue

            # 冲突校验
            conflict = (
                Reservation.objects.filter(
                    room=r.room,
                    date=r.date,
                    status__in=["APPROVED", "USED"],
                )
                .exclude(id=r.id)
                .filter(
                    start_hour__lt=r.end_hour,
                    end_hour__gt=r.start_hour,
                )
                .exists()
            )

            if conflict:
                continue

            r.status = "APPROVED"
            r.approve_time = now
            r.save()
            success += 1

        self.message_user(request, f"{success} 条预约审批通过")

    @admin.action(description="驳回预约")
    def reject_reservations(self, request, queryset):
        now = timezone.now()
        updated = queryset.filter(status="PENDING").update(
            status="REJECTED",
            reject_reason="管理员后台驳回",
            approve_time=now,
        )
        self.message_user(request, f"{updated} 条预约已驳回")

    actions = [approve_reservations, reject_reservations]

    # ---- 保存钩子 ----
    def save_model(self, request, obj, form, change):
        # ===== 新建预约 =====
        if not change:
            # 管理员代他人预约是允许的（user 字段由管理员选择）
            if obj.status == "APPROVED":
                obj.approve_time = timezone.now()

        # ===== 编辑预约 =====
        else:
            if obj.status in ["APPROVED", "REJECTED"] and not obj.approve_time:
                obj.approve_time = timezone.now()

        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form
