<template>
  <div class="page-container">
    <h2 class="page-title">我的预约记录</h2>

    <div v-if="reservations.length === 0" class="no-reservations">
      暂无预约记录
    </div>

    <div
      v-for="res in reservations"
      :key="res.id"
      class="reservation-card"
      :class="statusClass(res.status)"
    >
      <div class="card-header">
        <h3 class="room-name">{{ res.room }}</h3>
        <span class="status-tag" :style="{ backgroundColor: statusColor(res.status) }">
          {{ statusText(res.status) }}
        </span>
      </div>

      <div class="card-body">
        <div class="info-item">
          <span class="icon">📅</span>
          <span class="label">预定日期：</span>
          <span>{{ res.date }}</span>
        </div>
        <div class="info-item">
          <span class="icon">🕒</span>
          <span class="label">预定时间：</span>
          <span>{{ res.time }}</span>
        </div>
        <div v-if="res.topic" class="info-item">
          <span class="icon">📝</span>
          <span class="label">会议主题：</span>
          <span>{{ res.topic }}</span>
        </div>

        <div v-if="res.approve_time" class="info-item">
            <span class="icon">✅</span>
            <span class="label">审批时间：</span>
            <span>{{ $formatTime(res.approve_time) }}</span>
        </div>

        <div v-if="res.reject_reason" class="info-item reject-reason">
            <span class="icon">❌</span>
            <span class="label">驳回原因：</span>
            <span>{{ res.reject_reason }}</span>
        </div>
      </div>

      <div class="card-footer">
        <button
          v-if="canCancel(res.status)"
          class="btn btn-cancel"
          @click="cancel(res)"
        >
          取消预约
        </button>

        <button
          v-if="canConfirmUse(res)"
          class="btn btn-confirm"
          @click="confirm(res)"
        >
          确认使用
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  getMyReservations,
  cancelReservation,
  confirmUse
} from '@/api/reservations'

const reservations = ref([])

onMounted(async () => {
  reservations.value = await getMyReservations()
})

/* ---------- 状态显示 ---------- */

const statusText = status => {
  switch (status) {
    case 'PENDING': return '待审批'
    case 'APPROVED': return '已批准'
    case 'REJECTED': return '已驳回'
    case 'CANCELED': return '已取消'
    case 'USED': return '已使用'
    default: return status
  }
}

const statusColor = status => {
  switch (status) {
    case 'PENDING': return '#ff9800' // 橙色
    case 'APPROVED': return '#4caf50' // 绿色
    case 'REJECTED': return '#f44336' // 红色
    case 'CANCELED': return '#9e9e9e' // 灰色
    case 'USED': return '#2196f3' // 蓝色
    default: return '#333'
  }
}

// 为卡片添加一个基于状态的class，用于更精细的样式控制（比如给过去的预约一个置灰效果）
const statusClass = status => {
    if (status === 'CANCELED' || status === 'USED') {
        return 'is-past';
    }
    return '';
}


/* ---------- 按钮控制 ---------- */

const canCancel = status =>
  status === 'PENDING' || status === 'APPROVED'

const canConfirmUse = res => res.status === 'APPROVED'


/* ---------- 操作 ---------- */

const cancel = async res => {
  await cancelReservation(res.id)
  res.status = 'CANCELED'
}

const confirm = async res => {
  await confirmUse(res.id)
  res.status = 'USED'
}

// 模拟 $formatTime 函数，请根据你的项目实际情况调整
const $formatTime = (timeStr) => {
    if (!timeStr) return '';
    const date = new Date(timeStr);
    return date.toLocaleString();
}

</script>

<style scoped>
.page-container {
  padding: 20px 40px;
  background-color: #f7f8fa;
  min-height: 100vh;
}

.page-title {
  font-size: 24px;
  color: #333;
  margin-bottom: 24px;
}

.no-reservations {
  text-align: center;
  color: #999;
  font-size: 16px;
  padding: 40px;
}

.reservation-card {
  background-color: #fff;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  margin-bottom: 20px;
  padding: 20px;
  transition: box-shadow 0.3s ease, transform 0.3s ease;
  overflow: hidden;
  position: relative;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.reservation-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    transform: translateY(-2px);
}

/* 对于已取消或已使用的记录，降低其饱和度，视觉上弱化 */
.reservation-card.is-past {
    background-color: #f9f9f9;
    opacity: 0.8;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 16px;
  margin-bottom: 16px;
}

.room-name {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.status-tag {
  color: white;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: bold;
}

.card-body {
  font-size: 14px;
  color: #666;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.info-item:last-child {
    margin-bottom: 0;
}

.info-item .icon {
    margin-right: 10px;
    font-size: 16px;
}

.info-item .label {
  font-weight: 500;
  color: #333;
}

.reject-reason span:last-child {
    color: #f44336;
    font-weight: bold;
}

.card-footer {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn {
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.btn-cancel {
  background-color: #fff;
  color: #f44336;
  border: 1px solid #f44336;
}

.btn-cancel:hover {
  background-color: #f44336;
  color: #fff;
}

.btn-confirm {
  background-color: #4caf50;
  color: white;
  border: 1px solid #4caf50;
}

.btn-confirm:hover {
  background-color: #45a049;
}
</style>