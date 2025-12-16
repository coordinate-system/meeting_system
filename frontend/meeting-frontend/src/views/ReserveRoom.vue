<template>
  <div class="page-container">
    <div class="reservation-card">
      <h2 class="card-title">预约会议室</h2>
      <p class="card-subtitle">请选择日期、时间及与会人数，我们将为您筛选出可用的会议室。</p>

      <!-- 表单区域：采用新的“输入组”设计 -->
      <div class="form-container">
        <!-- 第一行：日期和人数 -->
        <div class="form-row">
          <!-- 统一边框的输入组 -->
          <div class="input-group">
            <div class="form-group">
              <label for="date">预约日期</label>
              <input id="date" type="date" v-model="date" class="grouped-input" />
            </div>
            <!-- 分隔线 -->
            <div class="input-divider"></div>
            <div class="form-group">
              <label for="people">会议人数</label>
              <input id="people" type="number" v-model="people" class="grouped-input" />
            </div>
          </div>
        </div>
        <!-- 第二行：开始时间和结束时间 -->
        <div class="form-row">
          <!-- 统一边框的输入组 -->
          <div class="input-group">
            <div class="form-group">
              <label for="start-time">开始时间</label>
              <select id="start-time" v-model="startHour" class="grouped-input">
                <option v-for="h in hours" :key="h" :value="h">{{ h }}:00</option>
              </select>
            </div>
            <!-- 分隔线 -->
            <div class="input-divider"></div>
            <div class="form-group">
              <label for="end-time">结束时间</label>
              <select id="end-time" v-model="endHour" class="grouped-input">
                <option v-for="h in hours" :key="h" :value="h">{{ h }}:00</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <button class="search-button" @click="searchRooms">筛选可用会议室</button>

      <!-- 结果展示区域 (保持不变) -->
      <hr class="divider" v-if="filteredRooms.length" />
      <div v-if="filteredRooms.length">
        <h3 class="results-title">可预约会议室</h3>
        <div v-for="room in filteredRooms" :key="room.id" class="room-item-card">
          <div class="room-info">
            <h4 class="room-name">{{ room.name }}<span v-if="room.room_no">({{ room.room_no }})</span></h4>
            <p class="room-capacity">可容纳 {{ room.capacity }} 人</p>
          </div>
          <button class="reserve-button" @click="goConfirm(room)">立即预约</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Script 部分无需改动
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { checkRooms } from '@/api/reservations'

const router = useRouter()
const date = ref('')
const startHour = ref(9)
const endHour = ref(10)
const people = ref(1)
const hours = Array.from({ length: 15 }, (_, i) => i + 8)
const filteredRooms = ref([])

const searchRooms = async () => {
  if (!date.value) {
    alert('请选择预约日期！')
    return
  }
  filteredRooms.value = await checkRooms({
    date: date.value,
    start_hour: startHour.value,
    end_hour: endHour.value,
    people: people.value
  })
}

const goConfirm = room => {
  router.push({
    path: '/reserve/confirm',
    query: {
      roomId: room.id,
      date: date.value,
      start: startHour.value,
      end: endHour.value,
      people: people.value
    }
  })
}
</script>

<style scoped>
/* 基础样式 (保持不变) */
.page-container {
  padding: 40px;
  background-color: #f0f2f5;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}
.reservation-card {
  width: 100%;
  max-width: 800px;
  background-color: #ffffff;
  border-radius: 12px;
  padding: 32px 40px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.card-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}
.card-subtitle {
  font-size: 14px;
  color: #888;
  margin-bottom: 30px;
}

/* --- 全新表单布局样式 --- */
.form-container {
  display: flex;
  flex-direction: column;
  gap: 24px; /* 加大行间距 */
  margin-bottom: 30px;
}

.form-row {
  display: flex;
}

/* 核心：输入组容器 */
.input-group {
  display: flex;
  width: 100%;
  border: 1px solid #dde1e6; /* 统一的外部边框 */
  border-radius: 8px; /* 统一的圆角 */
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  overflow: hidden; /* 确保内部元素的圆角正确显示 */
}

/* 核心：当输入组内任一元素被聚焦时，改变整个组的样式 */
.input-group:focus-within {
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1); /* 使用柔和的外辉光 */
}

/* 核心：组内的表单项 */
.form-group {
  flex: 1; /* 平分空间 */
  padding: 8px 12px; /* 内边距，用于放置标签和输入框 */
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-size: 12px; /* 调小标签字体 */
  color: #666;
  margin-bottom: 4px;
  font-weight: 500;
}

/* 核心：组内输入框的样式 */
.grouped-input {
  border: none; /* 移除自身边框 */
  outline: none; /* 移除自身outline */
  width: 100%;
  background-color: transparent; /* 背景透明 */
  padding: 0; /* 移除默认内边距 */
  font-size: 16px; /* 调大输入字体 */
  color: #333;
}

/* 核心：输入框之间的分隔线 */
.input-divider {
  width: 1px;
  background-color: #dde1e6;
  margin: 8px 0; /* 上下留出间距 */
  transition: background-color 0.2s ease;
}

/* 当聚焦时，分隔线也同步变色 (可选，细节优化) */
.input-group:focus-within .input-divider {
  background-color: #007bff;
}

/* 浏览器原生控件样式微调 */
input[type="number"] {
  -moz-appearance: textfield;
}
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
select.grouped-input {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%23343a40' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M2 5l6 6 6-6'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.5rem center;
  background-size: 16px 12px;
}


/* 搜索按钮样式 */
.search-button { width: 100%; padding: 12px; background-color: #007bff; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: 500; cursor: pointer; transition: background-color 0.3s; }
.search-button:hover { background-color: #0056b3; }
.divider { border: none; border-top: 1px solid #eee; margin: 30px 0; }
.results-title { font-size: 20px; color: #333; margin-bottom: 20px; }
.room-item-card { display: flex; justify-content: space-between; align-items: center; border: 1px solid #eee; padding: 16px; border-radius: 8px; margin-bottom: 16px; transition: box-shadow 0.3s, border-color 0.3s; }
.room-item-card:hover { border-color: #ddd; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); }
.room-name { font-size: 18px; font-weight: 600; margin: 0 0 8px 0; }
.room-capacity { font-size: 14px; color: #666; margin: 0; }
.reserve-button { padding: 8px 16px; background-color: #28a745; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; transition: background-color 0.3s; }
.reserve-button:hover { background-color: #218838; }
</style>