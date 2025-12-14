from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def room_list_view(request):
    """
    GET /api/rooms/list/
    """
    print("fetch room list")

    # ===== 数据库操作（暂时注释）=====
    # rooms = get_all_rooms()

    data = [
        {
            "id": 1,
            "name": "第一会议室",
            "room_no": "A101",
            "capacity": 20,
            "area": 40,
            "usage": "例会",
            "photo": "/media/rooms/room1.jpg",
            "is_available": True,
        }
    ]

    return Response({"code": 0, "msg": "ok", "data": data})
