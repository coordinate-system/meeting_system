<template>
  <div style="padding: 40px">
    <h2>会议室列表</h2>

    <div
      v-for="room in rooms"
      :key="room.id"
      style="border: 1px solid #ccc; padding: 16px; margin-bottom: 16px"
    >
      <h3>{{ room.name }}（{{ room.room_no }}）</h3>

      <p>人数：{{ room.capacity }} 人</p>
      <p>面积：{{ room.area }} ㎡</p>
      <p>用途：{{ room.usage }}</p>

      <p>
        状态：
        <span v-if="room.is_available" style="color: green">可预约</span>
        <span v-else style="color: red">不可预约</span>
      </p>

      <!-- ✅ 有图片才显示 -->
      <img
        v-if="room.photo"
        :src="room.photo"
        alt="会议室图片"
        style="width: 200px; margin-top: 10px"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getRooms } from '@/api/rooms'

const rooms = ref([])

onMounted(async () => {
  rooms.value = await getRooms()
})
</script>
