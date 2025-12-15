<template>
  <div>
    <!-- 顶部导航 -->
    <div style="padding: 16px; background: #eee; display: flex; align-items: center">
      <button @click="go('/user/rooms')">查看会议室</button>

      <button @click="go('/user/reserve')" style="margin-left: 10px">
        预约会议室
      </button>

      <button @click="go('/user/my')" style="margin-left: 10px">
        我的预约
      </button>

      <!-- ✅ 新增：退出登录（靠右） -->
      <button
        @click="handleLogout"
        style="margin-left: auto; color: #c00"
      >
        退出登录
      </button>
    </div>

    <!-- 页面内容 -->
    <router-view />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const go = path => {
  router.push(path)
}

/* ---------- 退出登录 ---------- */
const handleLogout = () => {
  if (confirm('确认退出登录吗？')) {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('username')

    router.push('/login')
  }
}
</script>
