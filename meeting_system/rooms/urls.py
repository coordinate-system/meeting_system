from django.urls import path
from .views import room_list_view

urlpatterns = [
    path("list/", room_list_view),
]
