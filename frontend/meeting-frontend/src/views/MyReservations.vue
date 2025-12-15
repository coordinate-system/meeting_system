<template>
  <div style="padding: 40px">
    <h2>我的预约记录</h2>

    <div
      v-for="res in reservations"
      :key="res.id"
      style="border: 1px solid #ccc; padding: 16px; margin-bottom: 16px"
    >
      <h3>{{ res.room_name }}</h3>

      <p>日期：{{ res.date }}</p>
      <p>时间：{{ res.time }}</p>
      <p>会议主题：{{ res.topic }}</p>

      <p>
        状态：
        <span :style="{ color: statusColor(res.status) }">
          {{ statusText(res.status) }}
        </span>
      </p>

      <p v-if="res.approve_time">
        审批时间：{{ res.approve_time }}
      </p>

      <p v-if="res.reject_reason" style="color: red">
        驳回原因：{{ res.reject_reason }}
      </p>

      <!-- 操作按钮 -->
      <div style="margin-top: 10px">
        <button
          v-if="canCancel(res.status)"
          @click="cancel(res)"
        >
          取消预约
        </button>

        <button
          v-if="canConfirmUse(res)"
          style="margin-left: 10px"
          @click="confirmUse(res)"
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

// 状态文字
const statusText = status => {
  switch (status) {
    case 'PENDING':
      return '待审批'
    case 'APPROVED':
      return '已批准'
    case 'REJECTED':
      return '已驳回'
    case 'CANCELED':
      return '已取消'
    case 'USED':
      return '已使用'
    default:
      return status
  }
}

// 状态颜色
const statusColor = status => {
  switch (status) {
    case 'PENDING':
      return 'orange'
    case 'APPROVED':
      return 'green'
    case 'REJECTED':
      return 'red'
    case 'CANCELED':
      return 'gray'
    case 'USED':
      return 'blue'
    default:
      return 'black'
  }
}

/* ---------- 按钮控制 ---------- */

const canCancel = status =>
  status === 'PENDING' || status === 'APPROVED'

// 只有“已批准”且未确认使用的才能确认
const canConfirmUse = res =>
  res.status === 'APPROVED'

/* ---------- 操作 ---------- */

const cancel = async res => {
  await cancelReservation(res.id)
  res.status = 'CANCELED'
}

const confirm = async res => {
  await confirmUse(res.id)
  res.status = 'USED'
}
</script>


