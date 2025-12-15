from datetime import datetime
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from reservations.models import Reservation

from rooms.models import MeetingRoom


def validate_date_and_time(reserve_date, start_hour, end_hour):
    today = timezone.localdate()
    now_hour = timezone.localtime().hour

    if reserve_date < today:
        raise ValueError("预约日期不能早于今天")

    if start_hour < 0 or end_hour > 24:
        raise ValueError("小时必须在 0-24 范围内")

    if start_hour >= end_hour:
        raise ValueError("结束时间必须晚于开始时间")

    if reserve_date == today and start_hour < now_hour:
        raise ValueError("当天预约开始时间不能早于当前时间")


# ==========================================
# Service Layer: 业务逻辑与数据访问
# ==========================================


def check_room_conflict(room_id: int, date: str, start: int, end: int) -> bool:
    """
    检查预约冲突
    True 表示有冲突，False 表示无冲突
    检查时间段和状态为 PENDING、APPROVED、USED 的预约是否冲突
    """
    # 冲突逻辑：(Existing Start < New End) AND (Existing End > New Start)
    # 引用原始逻辑
    conflict_exists = (
        Reservation.objects.filter(
            room_id=room_id, date=date, status__in=["PENDING", "APPROVED", "USED"]
        )
        .filter(start_hour__lt=end, end_hour__gt=start)
        .exists()
    )
    return conflict_exists


def filter_available_rooms(date: str, start: int, end: int, people: int):
    """筛选可用会议室"""
    # 1. 初筛：容量足够 且 状态为开放 的会议室
    # 引用原始逻辑
    candidates = MeetingRoom.objects.filter(capacity__gte=people, is_available=True)

    available_rooms = []

    # 2. 遍历检查每个会议室在指定时间段是否有冲突
    for room in candidates:
        if not check_room_conflict(room.id, date, start, end):
            available_rooms.append(
                {
                    "id": room.id,
                    "name": room.name,
                    "capacity": room.capacity,
                    "usage": room.usage,
                    "photo": room.photo,  # 假设 Model 有 photo 字段，前端可能需要
                }
            )
    return available_rooms


# ==========================================
# View Layer: 接口与请求处理
# ==========================================


@api_view(["POST"])
def check_available_view(request):
    """
    POST /api/reservations/check/
    """
    try:
        data = request.data

        if not data.get("date"):
            return Response({"code": 400, "msg": "日期不能为空", "data": None})

        try:
            reserve_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
            start = int(data.get("start_hour"))
            end = int(data.get("end_hour"))
            people = int(data.get("people"))
        except Exception:
            return Response({"code": 400, "msg": "参数格式错误", "data": None})

        if people <= 0:
            return Response({"code": 400, "msg": "参会人数必须大于 0", "data": None})

        validate_date_and_time(reserve_date, start, end)

        rooms = filter_available_rooms(reserve_date, start, end, people)

        return Response({"code": 0, "msg": "ok", "data": rooms})

    except ValueError as e:
        return Response({"code": 400, "msg": str(e), "data": None})
    except Exception as e:
        return Response({"code": 500, "msg": "服务器内部错误", "data": None})


@api_view(["POST"])
def create_reservation_view(request):
    """
    POST /api/reservations/create/
    """
    try:
        user = request.user
        data = request.data

        required = ["room_id", "date", "start_hour", "end_hour", "topic", "people"]
        for f in required:
            if not data.get(f):
                return Response({"code": 400, "msg": f"缺少参数: {f}", "data": None})

        try:
            room_id = int(data["room_id"])
            reserve_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
            start = int(data["start_hour"])
            end = int(data["end_hour"])
            people = int(data["people"])
        except Exception:
            return Response({"code": 400, "msg": "参数格式错误", "data": None})

        validate_date_and_time(reserve_date, start, end)

        room = MeetingRoom.objects.get(id=room_id, is_available=True)

        if people > room.capacity:
            return Response({"code": 400, "msg": "会议室容量不足", "data": None})

        # ===============================
        # 关键：原子事务
        # ===============================
        with transaction.atomic():
            # 对可能冲突的记录加锁
            conflict_qs = (
                Reservation.objects.select_for_update()
                .filter(
                    room=room,
                    date=reserve_date,
                    status__in=["PENDING", "APPROVED", "USED"],
                )
                .filter(start_hour__lt=end, end_hour__gt=start)
            )

            if conflict_qs.exists():
                return Response({"code": 409, "msg": "该时间段已被占用", "data": None})

            Reservation.objects.create(
                user=user,
                room=room,
                date=reserve_date,
                start_hour=start,
                end_hour=end,
                topic=data["topic"],
                status="PENDING",
            )

        return Response({"code": 0, "msg": "预约提交成功，等待审批", "data": None})

    except MeetingRoom.DoesNotExist:
        return Response({"code": 404, "msg": "会议室不存在或不可用", "data": None})
    except ValueError as e:
        return Response({"code": 400, "msg": str(e), "data": None})
    except Exception as e:
        return Response({"code": 500, "msg": "系统错误", "data": None})


@api_view(["POST"])
def my_reservations_view(request):
    user = request.user

    records = Reservation.objects.filter(user=user).order_by("-date", "-start_hour")

    data = [
        {
            "id": r.id,
            "room": str(r.room),
            "date": r.date,
            "time": f"{r.start_hour}:00 - {r.end_hour}:00",
            "status": r.status,
            "approve_time": r.approve_time,
            "reject_reason": r.reject_reason,
        }
        for r in records
    ]

    return Response({"code": 0, "msg": "ok", "data": data})


@api_view(["POST"])
def cancel_reservation_view(request, res_id):
    try:
        r = Reservation.objects.get(id=res_id)

        if r.user != request.user:
            return Response({"code": 403, "msg": "无权操作", "data": None})

        if r.status not in ["PENDING", "APPROVED"]:
            return Response({"code": 400, "msg": "当前状态不可取消", "data": None})

        r.status = "CANCELED"
        r.save()

        return Response({"code": 0, "msg": "预约已取消", "data": None})

    except Reservation.DoesNotExist:
        return Response({"code": 404, "msg": "预约不存在", "data": None})


from django.utils import timezone


@api_view(["POST"])
def confirm_use_view(request, res_id):
    try:
        r = Reservation.objects.get(id=res_id)

        if r.user != request.user:
            return Response({"code": 403, "msg": "无权操作", "data": None})

        if r.status != "APPROVED":
            return Response({"code": 400, "msg": "仅已审批可确认使用", "data": None})

        now = timezone.localtime()
        start_time = timezone.make_aware(
            datetime.combine(r.date, datetime.min.time())
        ) + timezone.timedelta(hours=r.start_hour)

        # 允许前后 1 小时
        if abs((now - start_time).total_seconds()) > 3600:
            return Response(
                {"code": 400, "msg": "不在允许确认使用的时间范围内", "data": None}
            )

        r.status = "USED"
        r.save()

        return Response({"code": 0, "msg": "确认使用成功", "data": None})

    except Reservation.DoesNotExist:
        return Response({"code": 404, "msg": "预约不存在", "data": None})
