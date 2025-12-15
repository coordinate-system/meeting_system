from rest_framework.decorators import api_view
from rest_framework.response import Response
from rooms.models import MeetingRoom
from .serializers import MeetingRoomSerializer


@api_view(["GET"])
def room_list_view(request):
    """
    GET /api/rooms/list/
    """
    rooms = MeetingRoom.objects.all()
    serializer = MeetingRoomSerializer(
        rooms,
        many=True,
        context={"request": request}  # ⭐ 关键
    )

    return Response({
        "code": 0,
        "msg": "ok",
        "data": serializer.data
    })
