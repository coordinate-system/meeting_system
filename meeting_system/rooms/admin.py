from django.contrib import admin
from django.utils.html import format_html
from .models import MeetingRoom


@admin.register(MeetingRoom)
class MeetingRoomAdmin(admin.ModelAdmin):
    # (功能 1, 7) 列表显示：名称、房号、容量、面积、用途、状态
    list_display = (
        "name",
        "room_no",
        "capacity",
        "area",
        "usage",
        "show_photo",
        "is_available",
    )

    # (功能 1) 筛选器：按状态和容量筛选
    list_filter = ("is_available", "capacity")

    # (功能 1) 搜索框：搜索名称和用途
    search_fields = ("name", "usage")

    # 允许在列表页直接修改是否可预约
    list_editable = ("is_available",)

    # (功能 1) 图片预览功能
    def show_photo(self, obj):
        if obj.photo:
            # 假设 photo 存的是 URL，如果是 ImageField 需要用 obj.photo.url
            return format_html(
                """
                <a href="{0}" target="_blank">
                    <img src="{0}"
                        style="
                            max-width: 120px;
                            max-height: 80px;
                            width: auto;
                            height: auto;
                            object-fit: contain;
                            border-radius: 4px;
                            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
                        "
                        loading="lazy"
                    />
                </a>
                """,
                obj.photo,
            )
        return "无图片"

    show_photo.short_description = "照片预览"

    # (功能 10) 自定义动作：批量设置为可预约
    @admin.action(description="批量设为可预约")
    def make_available(self, request, queryset):
        queryset.update(is_available=True)

    # (功能 10) 自定义动作：批量设为不可预约
    @admin.action(description="批量设为不可预约")
    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)

    actions = [make_available, make_unavailable]
