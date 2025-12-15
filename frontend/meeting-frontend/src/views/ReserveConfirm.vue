<template>
  <div style="padding: 40px">
    <h2>确认预约</h2>

    <p>会议室ID：{{ roomId }}</p>
    <p>日期：{{ date }}</p>
    <p>时间：{{ start }}:00 - {{ end }}:00</p>
    <p>参会人数：{{ people }} 人</p>

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
