<template>
  <div>
    <!-- 顶部导航 -->
    <header class="top-nav">
      <nav class="nav-links">
        <button @click="go('/user/rooms')" class="nav-button">查看会议室</button>
        <button @click="go('/user/reserve')" class="nav-button">预约会议室</button>
        <button @click="go('/user/my')" class="nav-button">我的预约</button>
      </nav>
      <button @click="handleLogout" class="logout-button">退出登录</button>
    </header>

    <!-- 页面内容 -->
    <main class="content-view">
      <router-view />
    </main>
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
  if (confirm('您确定要退出登录吗？')) {
    // 清理本地存储的用户信息
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('username')

    // 跳转到登录页面
    router.push('/login')
  }
}
</script>

<style scoped>
/* 顶部导航栏容器样式 */
.top-nav {
  display: flex;
  justify-content: space-between; /* 两端对齐 */
  align-items: center;
  padding: 12px 24px;
  background-color: #f8f9fa; /* 更柔和的背景色 */
  border-bottom: 1px solid #dee2e6; /* 添加底部边框，增加层次感 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); /* 添加轻微阴影 */
}

/* 导航链接区域 */
.nav-links {
  display: flex;
  gap: 15px; /* 使用 gap 属性设置按钮间距 */
}

/* 通用按钮样式 */
.nav-button {
  padding: 8px 16px;
  font-size: 14px;
  color: #333;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s, border-color 0.3s; /* 平滑过渡效果 */
}

/* 按钮鼠标悬停效果 */
.nav-button:hover {
  background-color: #e9ecef;
  border-color: #adb5bd;
}

/* 按钮激活（点击时）效果 */
.nav-button:active {
  background-color: #dee2e6;
  transform: translateY(1px); /* 轻微下沉效果 */
}

/* 退出登录按钮特定样式 */
.logout-button {
  padding: 8px 16px;
  font-size: 14px;
  color: #dc3545; /* 醒目的红色字体 */
  background-color: transparent; /* 透明背景 */
  border: 1px solid #dc3545;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

/* 退出登录按钮鼠标悬停效果 */
.logout-button:hover {
  background-color: #dc3545;
  color: #fff; /* 字体变白 */
}

/* 退出登录按钮激活（点击时）效果 */
.logout-button:active {
  background-color: #c82333;
  border-color: #c82333;
  transform: translateY(1px);
}

/* 页面主要内容区域 */
.content-view {
  padding: 20px;
}
</style>