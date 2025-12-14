from django.urls import path
from .views import (
    check_available_view,
    create_reservation_view,
    my_reservations_view,
    cancel_reservation_view,
    confirm_use_view,
)

urlpatterns = [
    path("check/", check_available_view),
    path("create/", create_reservation_view),
    path("my/", my_reservations_view),
    path("<int:res_id>/cancel", cancel_reservation_view),
    path("<int:res_id>/confirm", confirm_use_view),
]
