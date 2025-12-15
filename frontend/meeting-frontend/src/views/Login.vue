<template>
  <!-- 
    核心修改：删除了 .login-card 容器
    现在 .login-container 直接包含左右两个部分 
  -->
  <div class="login-container">
    <!-- 左侧：插画区域 -->
    <!-- 使用 :style 绑定背景图，这是最可靠的方式 -->
    <div 
      class="illustration-side"
      :style="{ backgroundImage: `url(${bgImg})` }"
    >
    </div>

    <!-- 右侧：表单区域 -->
    <div class="form-side">
      <div class="form-content">
        <h2 class="form-title">登录</h2>
        
        <form @submit.prevent="handleLogin">
          <!-- 账号输入 -->
          <div class="input-group">
            <label>账号</label>
            <input 
              type="text" 
              v-model="form.username" 
              required 
            />
          </div>

          <!-- 密码输入 -->
          <div class="input-group">
            <label>密码</label>
            <input 
              type="password" 
              v-model="form.password" 
              required 
            />
          </div>

          <!-- 错误提示 -->
          <div v-if="errorMessage" class="error-text">
            {{ errorMessage }}
          </div>

          <!-- 登录按钮 -->
          <button type="submit" :disabled="isLoading">
            {{ isLoading ? '登录中...' : '登录' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/api/auth' 
import bgImg from '@/assets/rooms/loginph.jpg' 

const router = useRouter()

const form = reactive({
  username: '',
  password: ''
})

const isLoading = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    // login() 直接返回 { access, refresh }
    const res = await login(form)

    // res 就是后端 data
    localStorage.setItem('access_token', res.access)
    localStorage.setItem('refresh_token', res.refresh)
    localStorage.setItem('username', form.username)

    if (form.username === 'admin') {
      router.push('/admin')
    } else {
      router.push('/user')
    }
  } catch (error) {
    errorMessage.value = error.msg || '账号或密码错误'
  } finally {
    isLoading.value = false
  }
}

</script>

<style scoped>
/* 1. 全局容器现在是主布局，而不是背景板 */
.login-container {
  display: flex; /* 改为 flex 布局，让左右两边并排 */
  min-height: 100vh;
  width: 100%;
  background-color: #fff; /* 给个白色底色，以防图片加载失败 */
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

/* 2. 卡片样式 (.login-card) -> 已被删除，所以这个 CSS 规则也删掉 */


/* 3. 左侧插画区 */
.illustration-side {
  width: 58%; /* 使用百分比，更具弹性 */
  height: 100vh; /* 高度占满整个视口 */
  /* background-image 属性已由 :style 接管，这里可以删除 */
  background-size: cover;
  background-position: center;
  position: relative;
  /* 平滑的渐变遮罩，模拟 B 站效果 */
  mask-image: linear-gradient(to right, black 85%, transparent 100%);
  -webkit-mask-image: linear-gradient(to right, black 85%, transparent 100%);
}

/* 4. 右侧表单区 */
.form-side {
  flex: 1; /* 自动占据剩余空间 */
  height: 100vh; /* 高度同样占满整个视口 */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 40px;
}

.form-content {
  width: 100%;
  max-width: 320px; /* 表单内容的最大宽度 */
}

/* 其他表单内部样式保持不变 */
.form-title{text-align:center;font-size:24px;color:#555;font-weight:500;margin-bottom:40px;letter-spacing:2px}
.input-group{margin-bottom:25px}
.input-group label{display:block;font-size:12px;color:#999;margin-bottom:8px;padding-left:5px}
.input-group input{width:100%;height:44px;border:1px solid #e7e7e7;border-radius:22px;padding:0 20px;font-size:14px;outline:none;transition:all .3s;box-sizing:border-box}
.input-group input:focus{border-color:#40485b}
button{width:100%;height:44px;background-color:#3f4d63;color:#fff;border:none;border-radius:22px;font-size:16px;cursor:pointer;margin-top:10px;transition:opacity .2s}
button:hover{opacity:.9}
button:disabled{background-color:#ccc;cursor:not-allowed}
.error-text{color:#ff4d4f;font-size:12px;margin-bottom:10px;text-align:center}


/* 5. 媒体查询 (适配小屏幕) */
@media (max-width: 900px) {
  /* 在手机上，隐藏图片，让表单区占满整个屏幕 */
  .illustration-side {
    display: none;
  }
  .form-side {
    width: 100%;
    padding: 0 20px; /* 调整内边距 */
  }
}
</style>
