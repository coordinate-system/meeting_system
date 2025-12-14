from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),  # 后台管理路由
    path("api/auth/", include("users.urls")),
    path("api/rooms/", include("rooms.urls")),
    path("api/reservations/", include("reservations.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
