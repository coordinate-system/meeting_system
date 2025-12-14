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

  /**
   * 调用登录接口
   * ⚠️ 注意：因为 request.js 已经 return res.data
   * 所以这里拿到的就是 { access, refresh }
   */
  const tokenData = await login({
    username: username.value,
    password: password.value
  })

  // ✅ 存 JWT（后续请求用）
  localStorage.setItem('access_token', tokenData.access)
  localStorage.setItem('refresh_token', tokenData.refresh)

  // ✅ 保留你原有逻辑（系统目前只有普通用户）
  localStorage.setItem(
    'user',
    JSON.stringify({
      username: username.value
    })
  )

  router.push('/user/rooms')
}
</script>
