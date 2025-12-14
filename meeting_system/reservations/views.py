import logging
from django.db import transaction, DatabaseError
from rest_framework.decorators import api_view
from rest_framework.response import Response

from reservations.models import Reservation
from rooms.models import MeetingRoom

logger = logging.getLogger(__name__)

# ==========================================
# Service Layer: 业务逻辑与数据访问
# ==========================================


def check_room_conflict(room_id: int, date: str, start: int, end: int) -> bool:
    """
    检查预约冲突
    True 表示有冲突，False 表示无冲突
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


def create_reservation_service(data: dict):
    """
    创建预约（带事务和冲突检查）
    """
    room_id = data.get("room_id")
    date = data.get("date")
    start = int(data.get("start_hour"))
    end = int(data.get("end_hour"))

    # 使用事务保证原子性
    with transaction.atomic():
        # 修复 Bug：在保存前必须再次检查冲突，防止并发写入导致的时间重叠
        # 原始代码缺少此步骤
        if check_room_conflict(room_id, date, start, end):
            raise ValueError("该会议室在此时段已被他人抢先预约，请刷新重试。")

        reservation = Reservation.objects.create(**data)
        return reservation


def get_user_reservations(user_id: int):
    """获取用户预约记录"""
    # 引用原始逻辑
    return list(
        Reservation.objects.filter(user_id=user_id)
        .order_by("-date", "-start_hour")
        .values(
            "id",
            "date",
            "start_hour",
            "end_hour",
            "status",
            "topic",
            "room__name",
            "room_id",
            "reject_reason",
        )
    )


# ==========================================
# View Layer: 接口与请求处理
# ==========================================


@api_view(["POST"])
def check_available_view(request):
    """
    POST /api/reservations/check/
    筛选可用会议室
    """
    try:
        data = request.data
        date = data.get("date")

        # 参数校验与类型转换
        try:
            start = int(data.get("start_hour"))
            end = int(data.get("end_hour"))
            people = int(data.get("people", 0))
        except (ValueError, TypeError):
            return Response({"code": 400, "msg": "时间或人数格式错误", "data": None})

        # 逻辑校验
        if not date:
            return Response({"code": 400, "msg": "日期不能为空", "data": None})
        if start >= end:
            return Response(
                {"code": 400, "msg": "结束时间必须晚于开始时间", "data": None}
            )

        # 调用业务逻辑
        rooms = filter_available_rooms(date, start, end, people)
        return Response({"code": 0, "msg": "ok", "data": rooms})

    except Exception as e:
        logger.error(f"查询可用会议室失败: {e}")
        return Response({"code": 500, "msg": "服务器内部错误", "data": None})


@api_view(["POST"])
def check_available_view(request):
    """
    POST /api/reservations/check/
    """
    try:
        data = request.data
        date = data.get("date")

        try:
            start = int(data.get("start_hour"))
            end = int(data.get("end_hour"))
            people = int(data.get("people", 0))
        except (ValueError, TypeError):
            return Response({"code": 400, "msg": "时间或人数格式错误", "data": None})

        if not date or start >= end:
            return Response({"code": 400, "msg": "参数校验失败", "data": None})

        rooms = filter_available_rooms(date, start, end, people)
        return Response({"code": 0, "msg": "ok", "data": rooms})

    except Exception as e:
        logger.error(f"查询可用会议室失败: {e}")
        return Response({"code": 500, "msg": "服务器内部错误", "data": None})


@api_view(["POST"])
def create_reservation_view(request):
    """
    POST /api/reservations/create/
    创建预约 - user_id 从 JWT 获取
    """
    try:
        data = request.data

        # ⚠️ 安全修复：从 JWT 获取 user_id
        user_id = request.user.id

        required_fields = ["room_id", "date", "start_hour", "end_hour", "topic"]

        for field in required_fields:
            if not data.get(field):
                return Response(
                    {"code": 400, "msg": f"缺少必填参数: {field}", "data": None}
                )

        if int(data.get("start_hour")) >= int(data.get("end_hour")):
            return Response({"code": 400, "msg": "时间设置无效", "data": None})

        # 构建完整数据，确保 user_id 正确
        full_data = {
            **data,
            "user_id": user_id,
            "status": "PENDING",  # 确保新创建的预约状态是待审批
        }

        create_reservation_service(full_data)

        return Response(
            {"code": 0, "msg": "预约申请提交成功，请等待审批", "data": None}
        )

    except ValueError as e:
        return Response({"code": 409, "msg": str(e), "data": None})
    except Exception as e:
        logger.error(f"创建预约未知错误: {e}")
        return Response({"code": 500, "msg": "系统繁忙，请稍后再试", "data": None})


@api_view(["POST"])
def my_reservations_view(request):
    """
    POST /api/reservations/my/
    获取当前登录用户的预约记录 - user_id 从 JWT 获取
    """
    # ⚠️ 安全修复：从 JWT 获取 user_id，忽略请求体中的 user_id 参数
    user_id = request.user.id

    try:
        records = get_user_reservations(user_id)
        return Response({"code": 0, "msg": "ok", "data": records})
    except Exception as e:
        return Response({"code": 500, "msg": str(e), "data": None})


@api_view(["POST"])
def cancel_reservation_view(request, res_id):
    """
    POST /api/reservations/{id}/cancel
    取消预约 - 必须是预约创建者
    """
    try:
        reservation = Reservation.objects.get(id=res_id)

        # ⚠️ 授权校验：确保用户只能取消自己的预约
        if reservation.user_id != request.user.id:
            return Response({"code": 403, "msg": "无权取消此预约", "data": None})

        if reservation.status in ["USED", "CANCELED", "REJECTED"]:
            return Response(
                {
                    "code": 400,
                    "msg": f"当前状态({reservation.get_status_display()})无法取消",
                    "data": None,
                }
            )

        reservation.status = "CANCELED"
        reservation.save()

        return Response({"code": 0, "msg": "预约已取消", "data": None})

    except Reservation.DoesNotExist:
        return Response({"code": 404, "msg": "预约记录不存在", "data": None})
    except Exception as e:
        return Response({"code": 500, "msg": "取消失败", "data": str(e)})


@api_view(["POST"])
def confirm_use_view(request, res_id):
    """
    POST /api/reservations/{id}/confirm
    确认使用 - 必须是预约创建者
    """
    try:
        reservation = Reservation.objects.get(id=res_id)

        # ⚠️ 授权校验：确保用户只能确认使用自己的预约
        if reservation.user_id != request.user.id:
            return Response({"code": 403, "msg": "无权确认使用此预约", "data": None})

        if reservation.status != "APPROVED":
            return Response(
                {"code": 400, "msg": "只有“已通过”的预约才能确认使用", "data": None}
            )

        reservation.status = "USED"
        reservation.save()

        return Response({"code": 0, "msg": "已确认使用会议室", "data": None})

    except Reservation.DoesNotExist:
        return Response({"code": 404, "msg": "预约记录不存在", "data": None})
    except Exception as e:
        return Response({"code": 500, "msg": "操作失败", "data": str(e)})
