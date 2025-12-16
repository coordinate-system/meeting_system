<template>
  <div class="room-list-container">
    <h2>会议室列表</h2>

    <div class="room-list">
      <!-- 如果列表为空，可以显示一个提示 -->
      <div v-if="rooms.length === 0" class="no-rooms-info">
        暂无会议室信息
      </div>

      <!-- 会议室卡片循环 -->
      <div
        v-for="room in rooms"
        :key="room.id"
        class="room-card"
      >
        <!-- 左侧：会议室基础信息 -->
        <div class="room-info">
          <h3 class="room-name">
            {{ room.name }}
            <span v-if="room.room_no" class="room-no">（{{ room.room_no }}）</span>
          </h3>

          <div class="room-details">
            <span v-if="room.capacity !== null && room.capacity !== undefined">
              人数：{{ room.capacity }} 人
            </span>
            <span v-if="room.area !== null && room.area !== undefined">
              面积：{{ room.area }} ㎡
            </span>
          </div>

          <p v-if="room.usage" class="room-usage">
            用途：{{ room.usage }}
          </p>

          <p class="room-status">
            状态：
            <span :class="{
              'status-available': room.is_available,
              'status-unavailable': !room.is_available,
            }">
              ● {{ room.is_available ? "可预约" : "不可预约" }}
            </span>
          </p>
        </div>

        <!-- 右侧：会议室图片 -->
        <div class="room-image-container">
          <img
            v-if="room.photo"
            :src="room.photo"
            alt="会议室图片"
            class="room-thumbnail"
            @click="openPreview(room.photo)"
          />
          <div v-else class="no-image-placeholder">暂无图片</div>
        </div>
      </div>
    </div>

    <!-- 图片放大预览 -->
    <div
      v-if="previewVisible"
      class="preview-mask"
      @click.self="closePreview"
    >
      <img :src="previewImage" class="preview-image" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getRooms } from '@/api/rooms' // 确保您的 API 路径是正确的

// 初始化一个空的 ref，用于存放从后端获取的会议室数据
const rooms = ref([])

// 在组件挂载后，调用 API 函数获取数据并填充到 rooms 中
onMounted(async () => {
  try {
    rooms.value = await getRooms()
  } catch (error) {
    console.error("获取会议室列表失败:", error);
    // 这里可以添加一些用户友好的错误提示
  }
})

/* ---------- 图片预览 (这部分逻辑保持不变) ---------- */
const previewVisible = ref(false)
const previewImage = ref('')

const openPreview = (img) => {
  previewImage.value = img
  previewVisible.value = true
  document.addEventListener('keydown', handleEsc)
}

const closePreview = () => {
  previewVisible.value = false
  previewImage.value = ''
  document.removeEventListener('keydown', handleEsc)
}

/* Esc 关闭 */
const handleEsc = (e) => {
  if (e.key === 'Escape') {
    closePreview()
  }
}

/* 防止组件卸载时监听残留 */
onUnmounted(() => {
  document.removeEventListener('keydown', handleEsc)
})
</script>

<style scoped>
.room-list-container {
  padding: 20px 40px;
  background-color: #f7f8fa;
  min-height: 100vh;
}

h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 24px;
}

.room-list {
  display: flex;
  flex-direction: column;
  gap: 20px; /* 卡片之间的间距 */
}

/* 会议室卡片 */
.room-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.room-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

/* 左侧信息 */
.room-info {
  flex: 1;
  padding-right: 24px;
}

.room-name {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 12px 0;
}

.room-no {
  font-size: 16px;
  color: #888;
}

.room-details {
  display: flex;
  gap: 24px;
  color: #555;
  font-size: 14px;
  margin-bottom: 12px;
}

.room-details span {
  display: flex;
  align-items: center;
}

.room-usage {
  color: #555;
  font-size: 14px;
  margin-bottom: 16px;
}

.room-status {
  font-size: 14px;
  color: #333;
}

.room-status span {
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 13px;
}

/* 状态颜色 */
.status-available {
  color: #1d9d74;
  background-color: #e8f5f1;
}

.status-unavailable {
  color: #d9534f;
  background-color: #fdf0f0;
}


/* 右侧图片 */
.room-image-container {
  width: 240px;
  height: 160px;
  flex-shrink: 0; /* 防止容器被压缩 */
  border-radius: 8px;
  overflow: hidden;
  background-color: #eee;
}

.room-thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保证图片不变形 */
  cursor: pointer;
  transition: transform 0.3s ease;
}

.room-thumbnail:hover {
  transform: scale(1.05);
}

.no-image-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  color: #999;
  font-size: 14px;
}

/* 列表为空时的提示 */
.no-rooms-info {
  text-align: center;
  color: #888;
  padding: 40px;
  background-color: #fff;
  border-radius: 8px;
}

/* 图片预览 */
.preview-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.preview-image {
  max-width: 90%;
  max-height: 90%;
  border-radius: 8px;
}
</style>