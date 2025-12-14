from django.urls import path
from .views import MeetingRoomListView


urlpatterns = [
    path("list/", MeetingRoomListView.as_view()),
]
