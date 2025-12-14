<template>
  <div>
    <!-- 顶部导航 -->
    <div style="padding: 16px; background: #eee">
      <button @click="go('/user/rooms')">查看会议室</button>
      <button @click="go('/user/reserve')" style="margin-left: 10px">
        预约会议室
      </button>
      <button @click="go('/user/my')" style="margin-left: 10px">
        我的预约
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
</script>
