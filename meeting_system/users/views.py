from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


# class UserInfoView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response({"username": request.user.username})


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    POST /api/auth/login/
    """
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"code": 4001, "msg": "用户名或密码错误", "data": None})

    # 生成 JWT
    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "code": 0,
            "msg": "ok",
            "data": {
                "user_id": user.id,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
        }
    )
