from rest_framework.decorators import api_view
from rest_framework.response import Response
from rooms.models import MeetingRoom


@api_view(["GET"])
def room_list_view(request):
    """
    GET /api/rooms/list/
    """

    return Response(
        {"code": 0, "msg": "ok", "data": list(MeetingRoom.objects.all().values())}
    )
