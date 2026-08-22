import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Dashboard', component: () => import('../views/Dashboard.vue'), meta: { title: '营运看板' } },
  { path: '/products', name: 'Products', component: () => import('../views/Products.vue'), meta: { title: '商品推荐' } },
  { path: '/customers', name: 'Customers', component: () => import('../views/Customers.vue'), meta: { title: '顾客经营' } },
  { path: '/inventory', name: 'Inventory', component: () => import('../views/Inventory.vue'), meta: { title: '库存管理' } },
  { path: '/chat', name: 'Chat', component: () => import('../views/Chat.vue'), meta: { title: '智能对话' } }
]

// hash 模式：保证在 GitHub Pages 等纯静态托管下刷新/深链不 404
const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
