from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def check_available_view(request):
    """
    POST /api/reservations/check/
    """
    date = request.data.get("date")
    start = request.data.get("start_hour")
    end = request.data.get("end_hour")
    people = request.data.get("people")

    print("check rooms:", date, start, end, people)

    # ===== 数据库操作（暂时注释）=====
    # rooms = filter_available_rooms(date, start, end, people)

    rooms = [{"room_id": 1, "name": "第一会议室", "capacity": 20}]

    return Response({"code": 0, "msg": "ok", "data": rooms})


@api_view(["POST"])
def create_reservation_view(request):
    """
    POST /api/reservations/create/
    """
    print("create reservation:", request.data)

    # ===== 数据库操作（暂时注释）=====
    # create_reservation(request.data)

    return Response({"code": 0, "msg": "预约创建成功", "data": None})


@api_view(["GET"])
def my_reservations_view(request):
    """
    GET /api/reservations/my/
    """
    user_id = 1  # 通常从登录态中获取
    print("get reservations for user:", user_id)

    # ===== 数据库操作（暂时注释）=====
    # records = get_user_reservations(user_id)

    records = [
        {
            "id": 10,
            "room_name": "第一会议室",
            "date": "2025-06-01",
            "time": "09:00-12:00",
            "status": "PENDING",
            "approve_time": None,
            "reject_reason": None,
        }
    ]

    return Response({"code": 0, "msg": "ok", "data": records})


@api_view(["POST"])
def cancel_reservation_view(request, res_id):
    """
    POST /api/reservations/{id}/cancel
    """
    print("cancel reservation:", res_id)

    # ===== 数据库操作（暂时注释）=====
    # cancel_reservation(res_id)

    return Response({"code": 0, "msg": "预约已取消", "data": None})


@api_view(["POST"])
def confirm_use_view(request, res_id):
    """
    POST /api/reservations/{id}/confirm
    """
    print("confirm use:", res_id)

    # ===== 数据库操作（暂时注释）=====
    # confirm_use(res_id)

    return Response({"code": 0, "msg": "已确认使用会议室", "data": None})
