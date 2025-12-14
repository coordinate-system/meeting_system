from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from dao.reservations_dao import *
from rest_framework.permissions import AllowAny


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

    rooms = filter_available_rooms(date, start, end, people)

    return Response({"code": 0, "msg": "ok", "data": rooms})


@api_view(["POST"])
def create_reservation_view(request):
    """
    POST /api/reservations/create/
    """
    print("create reservation:", request.data)

    create_reservation(request.data)

    return Response({"code": 0, "msg": "预约创建成功", "data": None})


@api_view(["POST"])
def my_reservations_view(request):
    """
    POST /api/reservations/my/
    """
    print("get reservations for user:", request.data.get("user_id"))

    records = get_user_reservations(request.data.get("user_id"))

    return Response({"code": 0, "msg": "ok", "data": records})


@api_view(["POST"])
def cancel_reservation_view(request, res_id):
    """
    POST /api/reservations/{id}/cancel
    """
    print("cancel reservation:", res_id)

    cancel_reservation(res_id)

    return Response({"code": 0, "msg": "预约已取消", "data": None})


@api_view(["POST"])
def confirm_use_view(request, res_id):
    """
    POST /api/reservations/{id}/confirm
    """
    print("confirm use:", res_id)

    confirm_use(res_id)

    return Response({"code": 0, "msg": "已确认使用会议室", "data": None})
