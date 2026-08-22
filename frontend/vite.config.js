import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { spawn } from 'child_process'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// GitHub Pages 部署时资源需带仓库名前缀；本地开发用根路径
const base = process.env.GITHUB_PAGES === 'true' ? '/smart-retail-agent/' : '/'

// 前端启动时自动拉起 FastAPI 后端（前后端一起启动），前端退出时自动停止后端
function autoStartBackend() {
  let proc = null
  return {
    name: 'auto-start-backend',
    // configureServer 返回的「post hook」在中间件安装完成后执行一次，此时 httpServer 已就绪
    configureServer(server) {
      return async () => {
        // 线上构建/部署（GitHub Pages）不启动本地后端
        if (process.env.GITHUB_PAGES === 'true') return
        // 本会话已启动过且仍在运行，不重复启动（防止 Vite 重启 dev server 时重复拉起）
        if (proc && proc.exitCode === null) {
          console.log('[backend] 后端已在运行，跳过自动启动')
          return
        }
        const backendDir = path.resolve(__dirname, '../backend')
        const pythonBin = process.platform === 'win32'
          ? path.resolve(backendDir, 'venv/Scripts/python.exe')
          : path.resolve(backendDir, 'venv/bin/python')
        // 直接启动，让 uvicorn 自行绑定 8000：启动需要约 1 秒，此时旧进程的端口已释放，天然无竞态
        proc = spawn(pythonBin, ['-m', 'uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8000'], {
          cwd: backendDir,
          stdio: 'inherit',
          shell: false
        })
        proc.on('error', (err) => {
          if (err.code === 'ENOENT') {
            console.error('[backend] 未找到后端 venv，请先执行安装：cd backend && python -m venv venv && venv\\Scripts\\pip install -r requirements.txt')
          } else {
            console.error('[backend] 后端启动失败:', err.message)
          }
          proc = null
        })
        proc.on('exit', (code) => {
          // uvicorn 自行退出（如 8000 端口已被其他服务占用）时给出提示
          if (code && code !== 0) {
            console.error('[backend] 后端进程退出 (code ' + code + ')。若提示端口被占用，说明 8000 端口已有服务在运行。')
          }
          proc = null
        })
        console.log('[backend] FastAPI 已随前端自动启动 → http://localhost:8000')
        // 前端停止时自动结束后端：dev server 关闭 + 进程退出双保险
        const cleanup = () => {
          if (proc) {
            proc.kill()
            console.log('[backend] 后端已随前端停止')
            proc = null
          }
        }
        server.httpServer?.on('close', cleanup)
        process.on('exit', cleanup)
      }
    }
  }
}

export default defineConfig({
  plugins: [vue(), autoStartBackend()],
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
