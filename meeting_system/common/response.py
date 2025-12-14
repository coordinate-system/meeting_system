from rest_framework.response import Response


def success(data=None, msg="ok"):
    return Response({"code": 0, "msg": msg, "data": data})


def error(code, msg):
    return Response({"code": code, "msg": msg, "data": None})
