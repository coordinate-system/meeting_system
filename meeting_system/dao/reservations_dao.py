from django.db.models import Q
from django.utils import timezone
from reservations.models import Reservation
from rooms.models import MeetingRoom

def check_room_conflict(room_id: int, date: str, start: int, end: int) -> bool:
    """
    检查预约冲突
    True 表示有冲突，False 表示无冲突
    """
    # 冲突逻辑：已存在的开始时间 < 新的结束时间 AND 已存在的结束时间 > 新的开始时间
    # 状态排除：CANCELED 和 REJECTED 的不占用时间
    conflict_exists = Reservation.objects.filter(
        room_id=room_id,
        date=date,
        status__in=['PENDING', 'APPROVED', 'USED']
    ).filter(
        start_hour__lt=end,
        end_hour__gt=start
    ).exists()
    
    return conflict_exists

def filter_available_rooms(date: str, start: int, end: int, people: int):
    """筛选可用会议室"""
    # 1. 初筛：容量足够 且 状态为开放 的会议室
    candidates = MeetingRoom.objects.filter(
        capacity__gte=people,
        is_available=True
    )
    
    available_rooms = []
    
    # 2. 遍历检查每个会议室在指定时间段是否有冲突
    for room in candidates:
        if not check_room_conflict(room.id, date, start, end):
            # 将模型对象转为字典返回，或者直接返回 ID
            # 这里为了方便展示，转化为字典
            room_dict = {
                "id": room.id,
                "name": room.name,
                "capacity": room.capacity,
                "usage": room.usage
            }
            available_rooms.append(room_dict)
            
    return available_rooms

def create_reservation(data: dict):
    """创建预约"""
    # data 必须包含 user_id, room_id, date, start_hour, end_hour
    return Reservation.objects.create(**data)

def get_user_reservations(user_id: int):
    """用户预约记录"""
    # 使用 values() 获取字典列表，包含关联的会议室名称
    return list(Reservation.objects.filter(user_id=user_id)
                .order_by('-date', '-start_hour')
                .values('id', 'date', 'start_hour', 'end_hour', 'status', 'topic', 
                        'room__name', 'room_id'))

def get_all_reservations():
    """管理查看全部"""
    return list(Reservation.objects.all()
                .order_by('-date', '-start_hour')
                .values('id', 'user__username', 'room__name', 'date', 
                        'start_hour', 'end_hour', 'status', 'topic'))

def approve_reservation(res_id: int, admin_id: int):
    """审批通过"""
    Reservation.objects.filter(id=res_id).update(
        status='APPROVED',
        approve_time=timezone.now()
    )

def reject_reservation(res_id: int, admin_id: int, reason: str):
    """审批驳回"""
    Reservation.objects.filter(id=res_id).update(
        status='REJECTED',
        reject_reason=reason,
        approve_time=timezone.now()
    )

def cancel_reservation(res_id: int):
    """取消预约"""
    Reservation.objects.filter(id=res_id).update(status='CANCELED')

def confirm_use(res_id: int):
    """确认使用"""
    Reservation.objects.filter(id=res_id).update(status='USED')