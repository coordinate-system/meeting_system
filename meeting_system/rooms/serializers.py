from rest_framework import serializers
from .models import MeetingRoom


class MeetingRoomSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = MeetingRoom
        fields = "__all__"

    def get_photo(self, obj):
        # photo 是字符串（如 "rooms/101.jpg" 或 "/media/rooms/101.jpg"）
        if not obj.photo:
            return None

        request = self.context.get("request")
        if not request:
            return obj.photo

        # 如果已经是完整 URL，直接返回
        if obj.photo.startswith("http"):
            return obj.photo
        
        # 已经包含 /media/
        if obj.photo.startswith("/media/"):
            return request.build_absolute_uri(obj.photo)

        # 如果是相对路径，手动拼 MEDIA_URL
        return request.build_absolute_uri("/media/" + obj.photo.lstrip("/"))
