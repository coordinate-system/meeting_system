import { createRouter, createWebHistory } from 'vue-router'

import Login from '@/views/Login.vue'

// ===== 用户端 =====
import UserLayout from '@/views/UserLayout.vue'
import RoomList from '@/views/RoomList.vue'
import ReserveRoom from '@/views/ReserveRoom.vue'
import ReserveConfirm from '@/views/ReserveConfirm.vue'
import MyReservations from '@/views/MyReservations.vue'



const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },

  // ===== 普通用户 =====
  {
    path: '/user',
    component: UserLayout,
    redirect: '/user/rooms',
    children: [
      { path: 'rooms', component: RoomList },
      { path: 'reserve', component: ReserveRoom },
      { path: 'my', component: MyReservations }
    ]
  },

  // 预约确认（单独页面）
  { path: '/reserve/confirm', component: ReserveConfirm },

  // ===== 管理员 =====
  {
    path: '/admin',
    beforeEnter: (to, from, next) => {
      // 直接跳转到 Django 后台
      window.location.href = 'http://127.0.0.1:8000/admin'
    }
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
