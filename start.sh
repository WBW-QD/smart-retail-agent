#!/bin/bash
# 智慧零售营运 Agent 一键启动脚本（跨平台：Windows Git Bash / Linux / macOS）
# Windows 用户也可双击 start.bat（内部调用本脚本）

echo "========================================="
echo "  智慧零售营运 Agent - 启动脚本"
echo "========================================="

# ---------- 平台检测 ----------
if [ "$(uname -s | cut -c1-5)" = "MINGW" ] || [ "$(uname -s | cut -c1-5)" = "MSYS" ]; then
  IS_WINDOWS=1
  PYTHON="python"                 # Windows 下用 python，无 python3 别名
  ACTIVATE="venv/Scripts/activate"
else
  IS_WINDOWS=0
  PYTHON="python3"
  ACTIVATE="venv/bin/activate"
fi

# 检查 Ollama
echo ""
echo "[1/4] 检查 Ollama 服务..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
  echo "  ✓ Ollama 服务运行中"
  curl -s http://localhost:11434/api/tags | $PYTHON -c "import sys,json; data=json.load(sys.stdin); print('  已安装模型:', ', '.join([m['name'] for m in data.get('models',[])]))" 2>/dev/null
else
  echo "  ✗ 未检测到 Ollama 服务，请先启动: ollama serve"
  echo "    拉取模型: ollama pull qwen2.5:7b"
fi

# 后端
echo ""
echo "[2/4] 启动后端 (FastAPI, 端口 8000)..."
cd backend
if [ ! -d "venv" ]; then
  echo "  创建虚拟环境..."
  $PYTHON -m venv venv
fi
source $ACTIVATE
python -m pip install -q -r requirements.txt 2>/dev/null
echo "  后端依赖安装完成"
# 后台启动后端
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo "  ✓ 后端已启动 (PID: $BACKEND_PID)"
cd ..

# 前端
echo ""
echo "[3/4] 启动前端 (Vue 3, 端口 5173)..."
cd frontend
if [ ! -d "node_modules" ]; then
  echo "  安装前端依赖..."
  npm install
fi
echo "  前端依赖安装完成"
npm run dev &
FRONTEND_PID=$!
echo "  ✓ 前端已启动 (PID: $FRONTEND_PID)"
cd ..

echo ""
echo "[4/4] 启动完成！"
echo "========================================="
echo "  前端地址: http://localhost:5173"
echo "  后端API:  http://localhost:8000/docs"
echo "  Ollama:   http://localhost:11434"
echo "========================================="
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待，捕获退出信号清理进程
# Windows 下用 taskkill /T 结束整个进程树（uvicorn --reload 与 npm 会派生子进程）
trap "echo ''; echo '正在停止服务...'; if [ $IS_WINDOWS = 1 ]; then taskkill //T //F //PID $BACKEND_PID //PID $FRONTEND_PID 2>/dev/null; else kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; fi; echo '已停止'; exit 0" INT TERM
wait
