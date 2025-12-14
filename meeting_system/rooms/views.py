from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MeetingRoom
from .serializers import MeetingRoomSerializer


class MeetingRoomListView(APIView):
    def get(self, request):
        rooms = MeetingRoom.objects.filter(is_available=True)
        serializer = MeetingRoomSerializer(rooms, many=True)
        return Response(serializer.data)
