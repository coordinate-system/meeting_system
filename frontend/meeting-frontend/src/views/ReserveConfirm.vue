<template>
  <div style="padding: 40px">
    <h2>确认预约</h2>

    <p>会议室ID：{{ roomId }}</p>
    <p>日期：{{ date }}</p>
    <p>时间：{{ start }}:00 - {{ end }}:00</p>

    <div style="margin-top: 20px">
      <label>会议主题：</label>
      <input v-model="topic" />
    </div>

    <button style="margin-top: 20px" @click="submit">
      确认预约
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createReservation } from '@/api/reservations'

const route = useRoute()
const router = useRouter()

const topic = ref('')

const submit = async () => {
  await createReservation({
    room_id: route.query.roomId,
    date: route.query.date,
    start_hour: route.query.start,
    end_hour: route.query.end,
    topic: topic.value
  })

  alert('预约成功，等待审批')
  router.push('/user/my')
}
</script>


