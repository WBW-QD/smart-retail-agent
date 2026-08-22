@echo off
rem 智慧零售营运 Agent - Windows 双击停止脚本
rem 依赖：已安装 Git Bash（bash 命令在 PATH 中）
cd /d "%~dp0"
echo 正在通过 Git Bash 停止服务...
bash stop.sh
pause
