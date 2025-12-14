from django.db import models


class MeetingRoom(models.Model):
    name = models.CharField(max_length=100)
    room_no = models.CharField(max_length=50)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
