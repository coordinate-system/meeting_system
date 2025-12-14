from django.urls import path
from .views import login_view  # , UserInfoView

urlpatterns = [
    path("login/", login_view),
    # path("me/", UserInfoView.as_view()),  # 需要 JWT
]
