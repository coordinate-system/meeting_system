from rooms.models import MeetingRoom

def get_all_rooms():
    """返回所有会议室"""
    # 返回 QuerySet 的字典形式，方便前端处理
    return list(MeetingRoom.objects.all().values())

def get_available_rooms():
    """返回可预约会议室"""
    return list(MeetingRoom.objects.filter(is_available=True).values())

def create_room(room_data: dict):
    """新增会议室"""
    # room_data 应该包含 name, capacity 等字段
    return MeetingRoom.objects.create(**room_data)

def update_room(room_id: int, room_data: dict):
    """修改会议室"""
    MeetingRoom.objects.filter(id=room_id).update(**room_data)

def delete_room(room_id: int):
    """删除会议室"""
    MeetingRoom.objects.filter(id=room_id).delete()

def set_room_status(room_id: int, is_available: bool):
    """设置会议室可预约状态"""
    # 使用 update 方法更高效，不需要先 get 再 save
    MeetingRoom.objects.filter(id=room_id).update(is_available=is_available)