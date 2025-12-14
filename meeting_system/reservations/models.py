from django.db import models
from django.contrib.auth.models import User

# 不需要 import MeetingRoom，直接用字符串关联即可

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('PENDING', '审核中'),
        ('APPROVED', '已通过'),
        ('REJECTED', '已驳回'),
        ('CANCELED', '已取消'),
        ('USED', '已使用'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="预约人")
    
    # 关键修改：这里指向 'rooms' 应用下的 'MeetingRoom' 模型
    room = models.ForeignKey('rooms.MeetingRoom', on_delete=models.CASCADE, verbose_name="会议室")
    
    date = models.DateField(verbose_name="预约日期")
    start_hour = models.IntegerField(verbose_name="开始时间(小时)")
    end_hour = models.IntegerField(verbose_name="结束时间(小时)")
    topic = models.CharField(max_length=255, null=True, blank=True, verbose_name="会议主题")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="状态")
    reject_reason = models.CharField(max_length=255, null=True, blank=True, verbose_name="驳回原因")
    approve_time = models.DateTimeField(null=True, blank=True, verbose_name="审批时间")

    class Meta:
        db_table = 'reservation'
        verbose_name = '预约记录'