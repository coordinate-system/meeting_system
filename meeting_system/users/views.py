from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


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
        return Response({"code": 404, "msg": "用户名或密码错误", "data": None})

    # 生成 JWT
    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "code": 0,
            "msg": "ok",
            "data": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
        }
    )
