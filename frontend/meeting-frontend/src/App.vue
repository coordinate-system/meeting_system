<template>
<h2>会议室列表</h2>
<ul>
<li v-for="room in rooms" :key="room.id">
{{ room.name }} - 容量 {{ room.capacity }}
</li>
</ul>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'


const rooms = ref([])


onMounted(async () => {
const res = await axios.get('http://127.0.0.1:8000/api/rooms/list/')
rooms.value = res.data
})
</script>