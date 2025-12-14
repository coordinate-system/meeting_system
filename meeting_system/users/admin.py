from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UsersProfile


# 定义内联显示，将 UsersProfile 嵌入到 User 的编辑页面中
class UsersProfileInline(admin.StackedInline):
    model = UsersProfile
    can_delete = False
    verbose_name_plural = "用户扩展信息"


# 继承原有的 UserAdmin
class UserAdmin(BaseUserAdmin):
    # 添加内联
    inlines = (UsersProfileInline,)

    list_display = (
        "username",
        "is_staff",
    )


# 必须先注销原有的 User 模型，再重新注册
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
