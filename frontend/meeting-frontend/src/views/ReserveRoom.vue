<template>
  <div style="padding: 40px">
    <h2>预约会议室</h2>

    <div style="margin-bottom: 20px">
      <label>日期：</label>
      <input type="date" v-model="date" />
    </div>

    <div style="margin-bottom: 20px">
      <label>开始时间：</label>
      <select v-model="startHour">
        <option v-for="h in hours" :key="h" :value="h">
          {{ h }}:00
        </option>
      </select>

      <label style="margin-left: 20px">结束时间：</label>
      <select v-model="endHour">
        <option v-for="h in hours" :key="h" :value="h">
          {{ h }}:00
        </option>
      </select>
    </div>

    <div style="margin-bottom: 20px">
      <label>会议人数：</label>
      <input type="number" v-model="people" />
    </div>

    <button @click="searchRooms">筛选会议室</button>

    <hr style="margin: 30px 0" />

    <div v-if="filteredRooms.length">
      <h3>可预约会议室</h3>

      <div
        v-for="room in filteredRooms"
        :key="room.id"
        style="border: 1px solid #ccc; padding: 16px; margin-bottom: 16px"
      >
        <h4>{{ room.name }}（{{ room.room_no }}）</h4>
        <p>可容纳 {{ room.capacity }} 人</p>

        <button @click="goConfirm(room)">预约该会议室</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { checkRooms } from '@/api/reservations'

const router = useRouter()

const date = ref('')
const startHour = ref(9)
const endHour = ref(10)
const people = ref(1)

const hours = Array.from({ length: 12 }, (_, i) => i + 8)
const filteredRooms = ref([])

const searchRooms = async () => {
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

