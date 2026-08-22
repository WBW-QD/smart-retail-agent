@echo off
rem 智慧零售营运 Agent - Windows 双击启动脚本
rem 依赖：已安装 Git Bash（bash 命令在 PATH 中）与 start.sh 同目录
cd /d "%~dp0"
echo 正在通过 Git Bash 启动项目...
bash start.sh
if errorlevel 1 (
  echo.
  echo 启动失败：请确认已安装 Git Bash，且 Ollama 服务已启动。
  pause
)
