<template>
  <div style="padding: 40px">
    <h2>会议室预约系统登录</h2>

    <div>
      <input v-model="username" placeholder="用户名" />
    </div>

    <div style="margin-top: 10px">
      <input v-model="password" type="password" placeholder="密码" />
    </div>

    <div style="margin-top: 20px">
      <button @click="handleLogin">登录</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/api/auth'

const username = ref('')
const password = ref('')
const router = useRouter()

const handleLogin = async () => {
  if (!username.value || !password.value) {
    alert('请输入用户名和密码')
    return
  }

  const user = await login({
    username: username.value,
    password: password.value
  })

  // 当前系统只有普通用户
  localStorage.setItem('user', JSON.stringify(user))
  router.push('/user/rooms')
}
</script>

