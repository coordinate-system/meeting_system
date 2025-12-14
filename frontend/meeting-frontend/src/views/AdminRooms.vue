<template>
  <div style="padding: 40px">
    <h2>会议室管理（管理员）</h2>

    <!-- 新增会议室 -->
    <h3>新增会议室</h3>

    <div style="margin-bottom: 20px">
      <input v-model="form.name" placeholder="会议室名称" />
      <input v-model="form.room_no" placeholder="房号" />
      <input type="number" v-model="form.capacity" placeholder="人数" />
      <input type="number" v-model="form.area" placeholder="面积" />
      <input v-model="form.usage" placeholder="用途" />
      <input v-model="form.photo" placeholder="图片路径" />
      <button @click="addRoom">添加</button>
    </div>

    <hr />

    <!-- 会议室列表 -->
    <h3>会议室列表</h3>

    <div
      v-for="room in rooms"
      :key="room.id"
      style="border: 1px solid #ccc; padding: 16px; margin-bottom: 16px"
    >
      <strong>{{ room.name }}（{{ room.room_no }}）</strong>
      <p>人数：{{ room.capacity }}</p>
      <p>面积：{{ room.area }}㎡</p>
      <p>用途：{{ room.usage }}</p>

      <p>
        状态：
        <span :style="{ color: room.is_available ? 'green' : 'red' }">
          {{ room.is_available ? '可预约' : '不可预约' }}
        </span>
      </p>

      <img
        :src="room.photo"
        style="width: 150px; display: block; margin: 10px 0"
      />

      <button @click="editRoom(room)">编辑</button>
      <button style="margin-left: 10px" @click="removeRoom(room.id)">
        删除
      </button>
      <button style="margin-left: 10px" @click="toggle(room)">
        切换状态
      </button>
    </div>

    <!-- 编辑弹窗 -->
    <div
      v-if="editing"
      style="border: 1px solid #666; padding: 20px"
    >
      <h3>编辑会议室</h3>

      <input v-model="editForm.name" placeholder="会议室名称" />
      <input v-model="editForm.room_no" placeholder="房号" />
      <input type="number" v-model="editForm.capacity" placeholder="人数" />
      <input type="number" v-model="editForm.area" placeholder="面积" />
      <input v-model="editForm.usage" placeholder="用途" />
      <input v-model="editForm.photo" placeholder="图片路径" />

      <div style="margin-top: 10px">
        <button @click="saveEdit">保存</button>
        <button style="margin-left: 10px" @click="cancelEdit">
          取消
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// mock 会议室
const rooms = ref([
  {
    id: 1,
    name: '第一会议室',
    room_no: 'A101',
    capacity: 20,
    area: 40,
    usage: '例会',
    photo: '/src/assets/rooms/room1.jpg',
    is_available: true
  },
  {
    id: 2,
    name: '第二会议室',
    room_no: 'B201',
    capacity: 10,
    area: 25,
    usage: '讨论',
    photo: '/src/assets/rooms/room2.jpg',
    is_available: false
  }
])

// 新增表单
const form = ref({
  name: '',
  room_no: '',
  capacity: 0,
  area: 0,
  usage: '',
  photo: ''
})

// 编辑状态
const editing = ref(false)
const editForm = ref({})
let editTarget = null

const addRoom = () => {
  rooms.value.push({
    ...form.value,
    id: Date.now(),
    is_available: true
  })

  Object.keys(form.value).forEach(k => form.value[k] = '')
}

const removeRoom = id => {
  rooms.value = rooms.value.filter(r => r.id !== id)
}

const toggle = room => {
  room.is_available = !room.is_available
}

const editRoom = room => {
  editing.value = true
  editTarget = room
  editForm.value = { ...room }
}

const saveEdit = () => {
  Object.assign(editTarget, editForm.value)
  editing.value = false
}

const cancelEdit = () => {
  editing.value = false
}
</script>
