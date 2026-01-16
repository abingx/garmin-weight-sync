#!/bin/bash
# Linux/macOS 快速打包脚本

echo "===================================="
echo "Garmin Weight Sync - 快速打包"
echo "===================================="
echo ""

# 检查 PyInstaller
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "PyInstaller 未安装，正在安装..."
    pip3 install pyinstaller
fi

echo ""
echo "开始打包..."
echo ""

python3 build.py

echo ""
echo "===================================="
echo "打包完成！"
echo "输出文件: dist/"
echo "===================================="
echo ""

# macOS: 如果有 .app 文件，说明打包成功
if [ -f "dist/GarminWeightSync.app" ]; then
    echo "✅ macOS App 已创建"
fi

if [ -f "dist/GarminWeightSync" ]; then
    echo "✅ 可执行文件已创建"
    echo ""
    echo "运行命令:"
    echo "  ./dist/GarminWeightSync"
fi
