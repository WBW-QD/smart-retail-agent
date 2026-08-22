#!/bin/bash
# 智慧零售营运 Agent 一键停止脚本（停止后端 8000 + 前端 5173）
# 跨平台：Windows Git Bash / Linux / macOS

echo "========================================="
echo "  智慧零售营运 Agent - 停止脚本"
echo "========================================="

# ---------- 平台检测 ----------
if [ "$(uname -s | cut -c1-5)" = "MINGW" ] || [ "$(uname -s | cut -c1-5)" = "MSYS" ]; then
  IS_WINDOWS=1
else
  IS_WINDOWS=0
fi

# 按端口停止监听进程（Windows 用 taskkill 结束进程树，Linux/macOS 用 lsof + kill）
stop_port() {
  local port=$1
  if [ $IS_WINDOWS = 1 ]; then
    local pids=$(netstat -ano | grep "LISTENING" | grep ":$port " | awk '{print $5}' | sort -u)
    if [ -z "$pids" ]; then
      echo "  端口 $port：无进程在监听"
      return
    fi
    for pid in $pids; do
      echo "  停止端口 $port 的进程 (PID $pid)"
      taskkill //F //T //PID $pid > /dev/null 2>&1 || true
    done
  else
    local pids=$(lsof -t -i:$port 2>/dev/null)
    if [ -z "$pids" ]; then
      echo "  端口 $port：无进程在监听"
      return
    fi
    for pid in $pids; do
      echo "  停止端口 $port 的进程 (PID $pid)"
      kill -9 $pid 2>/dev/null || true
    done
  fi
}

echo "[1/2] 停止后端 (FastAPI, 端口 8000)..."
stop_port 8000

echo "[2/2] 停止前端 (Vite, 端口 5173)..."
stop_port 5173

echo ""
echo "完成！本地服务已停止。"
echo "重新启动：./start.sh （Windows 双击 start.bat）"
