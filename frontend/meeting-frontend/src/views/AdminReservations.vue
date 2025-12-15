<template>
  <div style="padding: 40px">
    <h2>预约审批（管理员）</h2>

    <div
      v-for="res in reservations"
      :key="res.id"
      style="border: 1px solid #ccc; padding: 16px; margin-bottom: 16px"
    >
      <h3>{{ res.room_name }}</h3>

      <p>申请人：{{ res.user }}</p>
      <p>日期：{{ res.date }}</p>
      <p>时间：{{ res.time }}</p>
      <p>会议主题：{{ res.topic }}</p>

      <p>
        状态：
        <strong :style="{ color: statusColor(res.status) }">
          {{ statusText(res.status) }}
        </strong>
      </p>

      <p v-if="res.approve_time">
        审批时间：{{ $formatTime(res.approve_time) }}
      </p>

      <p v-if="res.reject_reason" style="color: red">
        驳回原因：{{ res.reject_reason }}
      </p>

      <!-- 管理员操作 -->
      <div v-if="res.status === 'PENDING'" style="margin-top: 10px">
        <button @click="approve(res)">通过</button>
        <button style="margin-left: 10px" @click="openReject(res)">
          驳回
        </button>
      </div>
    </div>

    <!-- 驳回弹窗 -->
    <div v-if="showReject" style="border: 1px solid #666; padding: 20px">
      <h3>驳回预约</h3>
      <textarea
        v-model="rejectReason"
        placeholder="请输入驳回理由"
        rows="3"
        style="width: 100%"
      ></textarea>

      <div style="margin-top: 10px">
        <button @click="confirmReject">确认驳回</button>
        <button style="margin-left: 10px" @click="cancelReject">
          取消
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 🚧 mock 全部预约数据
const reservations = ref([
  {
    id: 1,
    user: 'user1',
    room_name: '第一会议室',
    date: '2025-06-01',
    time: '09:00 - 12:00',
    topic: '项目评审',
    status: 'PENDING',
    approve_time: null,
    reject_reason: null
  },
  {
    id: 2,
    user: 'user2',
    room_name: '第二会议室',
    date: '2025-05-20',
    time: '14:00 - 16:00',
    topic: '组会',
    status: 'APPROVED',
    approve_time: '2025-05-18 10:30',
    reject_reason: null
  }
])

const showReject = ref(false)
const rejectReason = ref('')
const current = ref(null)

const statusText = s => ({
  PENDING: '待审批',
  APPROVED: '已通过',
  REJECTED: '已驳回',
  CANCELED: '已取消',
  USED: '已使用'
}[s])

const statusColor = s => ({
  PENDING: 'orange',
  APPROVED: 'green',
  REJECTED: 'red',
  CANCELED: 'gray',
  USED: 'blue'
}[s])

const approve = res => {
  res.status = 'APPROVED'
  res.approve_time = new Date().toLocaleString()
  alert('已通过预约')
}

const openReject = res => {
  current.value = res
  rejectReason.value = ''
  showReject.value = true
}

const confirmReject = () => {
  current.value.status = 'REJECTED'
  current.value.reject_reason = rejectReason.value
  current.value.approve_time = new Date().toLocaleString()
  showReject.value = false
  alert('已驳回预约')
}

const cancelReject = () => {
  showReject.value = false
}
</script>
