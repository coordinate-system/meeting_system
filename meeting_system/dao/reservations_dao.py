from django.db.models import Q
from django.utils import timezone
from reservations.models import Reservation
from rooms.models import MeetingRoom


def get_all_reservations():
    """管理查看全部"""
    return list(
        Reservation.objects.all()
        .order_by("-date", "-start_hour")
        .values(
            "id",
            "user__username",
            "room__name",
            "date",
            "start_hour",
            "end_hour",
            "status",
            "topic",
        )
    )


def approve_reservation(res_id: int, admin_id: int):
    """审批通过"""
    Reservation.objects.filter(id=res_id).update(
        status="APPROVED", approve_time=timezone.now()
    )


def reject_reservation(res_id: int, admin_id: int, reason: str):
    """审批驳回"""
    Reservation.objects.filter(id=res_id).update(
        status="REJECTED", reject_reason=reason, approve_time=timezone.now()
    )
