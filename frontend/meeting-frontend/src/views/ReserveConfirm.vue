<template>
  <div class="page-container">
    <div class="confirm-card">
      <h2 class="card-title">确认预约信息</h2>

      <div class="info-grid">
        <div class="info-item">
          <label>会议室 ID:</label>
          <span>{{ roomId }}</span>
        </div>
        <div class="info-item">
          <label>预定日期:</label>
          <span>{{ date }}</span>
        </div>
        <div class="info-item">
          <label>预定时间:</label>
          <span>{{ start }}:00 - {{ end }}:00</span>
        </div>
        <div class="info-item">
          <label>参会人数:</label>
          <span>{{ people }} 人</span>
        </div>
      </div>

      <div class="topic-section">
        <label for="topic-input">会议主题:</label>
        <input id="topic-input" v-model="topic" placeholder="请输入会议主题" />
      </div>

      <button class="submit-button" @click="submit">
        确认并提交预约
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createReservation } from '@/api/reservations'

const route = useRoute()
const router = useRouter()

// ⚠️ query 里的值全是字符串，必要的转成 Number
const roomId = ref(Number(route.query.roomId))
const date = ref(route.query.date)
const start = ref(Number(route.query.start))
const end = ref(Number(route.query.end))
const people = ref(Number(route.query.people)) 
const topic = ref('')

const submit = async () => {
  await createReservation({
    room_id: roomId.value,
    date: date.value,
    start_hour: start.value,
    end_hour: end.value,
    people: people.value,
    topic: topic.value
  })

  alert('预约成功，等待审批')
  router.push('/user/my')
}
</script>

<style scoped>
/* 全局页面容器 */
.page-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  padding: 40px;
  box-sizing: border-box;
}

/* 核心卡片设计 */
.confirm-card {
  width: 100%;
  max-width: 500px;
  background-color: #ffffff;
  border-radius: 16px; /* 更大的圆角 */
  padding: 32px;
  box-shadow: 
    0 8px 24px rgba(0, 0, 0, 0.1), /* 主要的阴影 */
    0 0 40px rgba(66, 133, 244, 0.15); /* 蓝色辉光效果 */
  border: 1px solid #e8e8e8;
  transition: all 0.3s ease;
}

.confirm-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 12px 32px rgba(0, 0, 0, 0.12),
    0 0 50px rgba(66, 133, 244, 0.2);
}

/* 卡片标题 */
.card-title {
  text-align: center;
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-top: 0;
  margin-bottom: 28px;
}

/* 信息网格布局 */
.info-grid {
  display: grid;
  grid-template-columns: 1fr; /* 单列布局，适用于所有屏幕 */
  gap: 16px; /* 项目之间的间隙 */
  margin-bottom: 24px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #eee;
}

.info-item label {
  font-weight: 600;
  color: #555;
}

.info-item span {
  font-size: 16px;
  color: #333;
  background-color: #e9effc; /* 给数值一个淡淡的背景色 */
  padding: 4px 10px;
  border-radius: 6px;
}

/* 会议主题部分 */
.topic-section {
  margin-top: 20px;
}

.topic-section label {
  display: block;
  font-weight: 600;
  color: #555;
  margin-bottom: 8px;
}

#topic-input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-sizing: border-box;
  transition: border-color 0.3s, box-shadow 0.3s;
}

#topic-input:focus {
  outline: none;
  border-color: #4285f4; /* 主题色 */
  box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.2);
}

#topic-input::placeholder {
  color: #aaa;
}

/* 提交按钮 */
.submit-button {
  width: 100%;
  padding: 14px;
  margin-top: 30px;
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  background-image: linear-gradient(45deg, #4285f4, #5a95f5);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(66, 133, 244, 0.3);
}

.submit-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(66, 133, 244, 0.4);
}
</style>