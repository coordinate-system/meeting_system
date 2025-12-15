<template>
  <div style="padding: 40px">
    <h2>会议室列表</h2>

    <div
      v-for="room in rooms"
      :key="room.id"
      style="border: 1px solid #ccc; padding: 16px; margin-bottom: 16px"
    >
      <h3>
        {{ room.name }}
        <span v-if="room.room_no">（{{ room.room_no }}）</span>
      </h3>

      <p v-if="room.capacity !== null && room.capacity !== undefined">
        人数：{{ room.capacity }} 人
      </p>

      <p v-if="room.area !== null && room.area !== undefined">
        面积：{{ room.area }} ㎡
      </p>

      <p v-if="room.usage">
        用途：{{ room.usage }}
      </p>

      <p>
        状态：
        <span v-if="room.is_available" style="color: green">可预约</span>
        <span v-else style="color: red">不可预约</span>
      </p>

      <!-- 缩略图 -->
      <img
        v-if="room.photo"
        :src="room.photo"
        alt="会议室图片"
        style="width: 200px; margin-top: 10px; cursor: pointer"
        @click="openPreview(room.photo)"
      />
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
import { getRooms } from '@/api/rooms'

const rooms = ref([])

onMounted(async () => {
  rooms.value = await getRooms()
})

/* ---------- 图片预览 ---------- */
const previewVisible = ref(false)
const previewImage = ref('')

const openPreview = img => {
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
const handleEsc = e => {
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
