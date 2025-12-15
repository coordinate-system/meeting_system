import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { formatTime } from '@/utils/time'
const app = createApp(App)
app.config.globalProperties.$formatTime = formatTime
app.use(router)
app.mount('#app')
