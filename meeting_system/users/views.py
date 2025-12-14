from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def login_view(request):
    """
    POST /api/auth/login/
    """
    username = request.data.get("username")
    password = request.data.get("password")

    print("login attempt:", username, password)

    # ===== 真实逻辑（暂时注释）=====
    # user = authenticate(username=username, password=password)
    # if not user:
    #     return Response({"code": 4001, "msg": "用户名或密码错误", "data": None})

    # user_id 需要从数据库中获取并加密，这里暂时写死为 1
    return Response(
        {"code": 0, "msg": "ok", "data": {"user_id": 1, "username": username}}
    )
