<template>
  <div style="padding: 40px">
    <h2>管理员后台</h2>

    <!-- 后台导航 -->
    <div style="margin-bottom: 20px">
      <router-link to="/admin/reservations">预约审批</router-link>
      |
      <router-link to="/admin/rooms">会议室管理</router-link>
    </div>

    <!-- 子页面出口 -->
    <router-view />
  </div>
</template>

<script setup>
</script>
