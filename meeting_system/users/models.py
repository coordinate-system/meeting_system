from django.db import models
from django.contrib.auth.models import User

class UsersProfile(models.Model):
    # 对应 SQL: users_profile 表
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')

    class Meta:
        db_table = 'users_profile'
        verbose_name = '用户扩展信息'
