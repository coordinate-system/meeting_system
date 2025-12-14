from django.db import models

class MeetingRoom(models.Model):
    # 对应 SQL: meeting_room 表
    name = models.CharField(max_length=100, verbose_name="名称")
    room_no = models.CharField(max_length=50, null=True, blank=True, verbose_name="房号")
    capacity = models.IntegerField(default=0, verbose_name="容纳人数")
    area = models.FloatField(default=0.0, verbose_name="面积")
    usage = models.CharField(max_length=255, null=True, blank=True, verbose_name="用途")
    photo = models.CharField(max_length=500, null=True, blank=True, verbose_name="图片URL")
    is_available = models.BooleanField(default=True, verbose_name="是否可预约")

    class Meta:
        db_table = 'meeting_room'
        verbose_name = '会议室'