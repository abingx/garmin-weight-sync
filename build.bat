@echo off
REM Windows 快速打包脚本

echo ====================================
echo Garmin Weight Sync - 快速打包
echo ====================================
echo.

REM 检查 PyInstaller
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller 未安装，正在安装...
    pip install pyinstaller
)

echo.
echo 开始打包...
echo.

python build.py

echo.
echo ====================================
echo 打包完成！
echo 输出文件: dist\
echo ====================================
echo.
pause
