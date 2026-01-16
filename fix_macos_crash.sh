#!/bin/bash
# macOS 闪退问题自动修复脚本

set -e

echo "============================================================"
echo "Garmin Weight Sync - macOS 闪退修复"
echo "============================================================"
echo ""

# 检查是否在项目根目录
if [ ! -f "build.py" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

# 步骤 1: 清理旧的打包文件
echo "【步骤 1/4】清理旧的打包文件..."
rm -rf build dist
echo "✅ 清理完成"
echo ""

# 步骤 2: 检查虚拟环境
echo "【步骤 2/4】检查虚拟环境..."
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ 虚拟环境: $VIRTUAL_ENV"
else
    echo "⚠️  未检测到虚拟环境"
    echo "   建议在虚拟环境中运行"
    echo ""
fi

# 步骤 3: 安装可能缺失的依赖
echo "【步骤 3/4】检查并安装缺失的依赖..."
pip install -q jaraco.classes jaraco.context jaraco.functools 2>/dev/null || echo "   (依赖已存在或安装失败，继续...)"
pip install -q importlib-metadata 2>/dev/null || echo "   (依赖已存在或安装失败，继续...)"
echo "✅ 依赖检查完成"
echo ""

# 步骤 4: 重新打包
echo "【步骤 4/4】重新打包..."
echo "   选择 1 - GUI 版本"
echo ""

# 使用 expect 自动输入 1（如果安装了 expect）
if command -v expect &> /dev/null; then
    expect << EOF
set timeout 300
spawn python build.py
expect "请输入选项"
send "1\r"
expect eof
EOF
else
    # 否则手动运行
    python build.py
fi

echo ""

# 步骤 5: 解除 macOS 隔离属性
echo "【步骤 5/5】解除 macOS 隔离属性..."
if [ -f "dist/GarminWeightSync" ]; then
    xattr -cr dist/GarminWeightSync
    echo "✅ 已解除: dist/GarminWeightSync"
fi

if [ -d "dist/GarminWeightSync.app" ]; then
    xattr -cr dist/GarminWeightSync.app
    echo "✅ 已解除: dist/GarminWeightSync.app"
fi

echo ""
echo "============================================================"
echo "✅ 修复完成！"
echo "============================================================"
echo ""
echo "现在可以运行："
echo "  ./dist/GarminWeightSync           (命令行)"
echo "  open dist/GarminWeightSync.app    (GUI)"
echo "  或双击 dist/GarminWeightSync.app"
echo ""
echo "如果还有问题，请查看:"
echo "  FIX_MACOS_CRASH.md"
echo ""
