import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// GitHub Pages 部署时资源需带仓库名前缀；本地开发用根路径
const base = process.env.GITHUB_PAGES === 'true' ? '/smart-retail-agent/' : '/'

export default defineConfig({
  plugins: [vue()],
  base,
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
