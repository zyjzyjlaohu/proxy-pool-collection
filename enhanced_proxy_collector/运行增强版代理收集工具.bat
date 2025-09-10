@echo off
chcp 65001 >nul

:: 检查Python环境
python --version >nul 2>nul
if %errorlevel% neq 0 (
echo 未找到Python环境，请先安装Python
pause
exit /b 1
)

:: 检查pip
pip --version >nul 2>nul
if %errorlevel% neq 0 (
echo 未找到pip，请先安装pip
pause
exit /b 1
)

:: 安装依赖
pip install requests >nul 2>nul
if %errorlevel% neq 0 (
echo 安装requests依赖失败，请手动安装：pip install requests
pause
exit /b 1
)

:: 运行代理收集工具
echo 开始运行增强版代理收集工具...
echo 这可能需要一段时间，请耐心等待...
python enhanced_proxy_collector.py

:: 等待用户输入
pause
