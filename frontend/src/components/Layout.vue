<template>
  <el-container class="layout">
    <el-aside width="220px" class="sidebar">
      <div class="logo">
        <el-icon :size="24" color="#409EFF"><ShoppingCart /></el-icon>
        <span>智慧零售Agent</span>
      </div>
      <el-menu :default-active="activeMenu" router class="nav-menu">
        <el-menu-item index="/">
          <el-icon><DataAnalysis /></el-icon>
          <span>营运看板</span>
        </el-menu-item>
        <el-menu-item index="/products">
          <el-icon><Goods /></el-icon>
          <span>商品推荐</span>
        </el-menu-item>
        <el-menu-item index="/customers">
          <el-icon><User /></el-icon>
          <span>顾客经营</span>
        </el-menu-item>
        <el-menu-item index="/inventory">
          <el-icon><Box /></el-icon>
          <span>库存管理</span>
        </el-menu-item>
        <el-menu-item index="/chat">
          <el-icon><ChatDotRound /></el-icon>
          <span>智能对话</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <span class="page-title">{{ currentTitle }}</span>
        <el-button type="primary" circle @click="chatVisible = !chatVisible">
          <el-icon><ChatDotRound /></el-icon>
        </el-button>
      </el-header>
      <el-main class="main-content">
        <!-- GitHub Pages 静态演示提示条（仅线上部署时显示） -->
        <el-alert
          v-if="isPagesDemo"
          type="warning"
          show-icon
          :closable="false"
          title="当前为 GitHub Pages 静态演示"
          description="AI 对话、数据看板、商品推荐等动态功能需在本地运行后端 + Ollama 才能使用。"
          class="pages-banner"
        />
        <router-view />
      </el-main>
    </el-container>

    <ChatSidebar v-model:visible="chatVisible" />
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ShoppingCart, DataAnalysis, Goods, User, Box, ChatDotRound } from '@element-plus/icons-vue'
import ChatSidebar from './ChatSidebar.vue'

const route = useRoute()
const chatVisible = ref(false)
const activeMenu = computed(() => route.path)
const currentTitle = computed(() => route.meta.title || '智慧零售营运Agent')
// 仅当运行在 GitHub Pages 域名下（xxx.github.io）时展示静态演示提示
const isPagesDemo = typeof window !== 'undefined' && window.location.hostname.endsWith('github.io')
</script>

<style scoped>
.layout { height: 100vh; }
.sidebar { background: #1f2937; color: #fff; }
.logo { display: flex; align-items: center; gap: 10px; padding: 20px; font-size: 16px; font-weight: bold; border-bottom: 1px solid #374151; }
.nav-menu { border-right: none; background: #1f2937; }
.nav-menu :deep(.el-menu-item) { color: #d1d5db; }
.nav-menu :deep(.el-menu-item.is-active) { background: #409EFF; color: #fff; }
.nav-menu :deep(.el-menu-item:hover) { background: #374151; }
.header { display: flex; justify-content: space-between; align-items: center; background: #fff; border-bottom: 1px solid #e5e7eb; padding: 0 24px; }
.page-title { font-size: 18px; font-weight: 600; color: #1f2937; }
.main-content { background: #f3f4f6; padding: 24px; overflow-y: auto; }
.pages-banner { margin-bottom: 16px; }
</style>
