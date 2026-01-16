#!/bin/bash
# Garmin Weight Sync - 环境设置和打包脚本

set -e  # 遇到错误立即退出

echo "============================================================"
echo "Garmin Weight Sync - 环境设置和打包"
echo "============================================================"
echo ""

# 检查 Python 版本
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "检测到 Python 版本: $PYTHON_VERSION"

# 检查是否需要升级 pip
echo ""
echo "【步骤 1/5】检查 pip 版本..."
pip3 install --upgrade pip

# 安装 GUI 依赖
echo ""
echo "【步骤 2/5】安装 GUI 依赖..."
pip3 install -r requirements-gui.txt

# 验证安装
echo ""
echo "【步骤 3/5】验证安装..."
python3 -c "import PyQt6; print(f'✅ PyQt6 版本: {PyQt6.Qt.PYQT_VERSION_STR}')"
python3 -c "import PyInstaller; print(f'✅ PyInstaller 版本: {PyInstaller.__version__}')"

# 检查源文件
echo ""
echo "【步骤 4/5】检查源文件..."
if [ -f "src/gui/main.py" ]; then
    echo "✅ GUI 入口文件存在"
else
    echo "❌ GUI 入口文件不存在"
    exit 1
fi

if [ -f "src/main.py" ]; then
    echo "✅ CLI 入口文件存在"
else
    echo "❌ CLI 入口文件不存在"
    exit 1
fi

# 清理旧的打包文件
echo ""
echo "【步骤 5/5】清理旧的打包文件..."
rm -rf build dist
echo "✅ 清理完成"

echo ""
echo "============================================================"
echo "✅ 环境设置完成！"
echo "============================================================"
echo ""
echo "现在可以运行打包脚本："
echo "  python3 build.py"
echo ""
echo "或直接运行 GUI 应用（测试）："
echo "  python3 src/gui/main.py"
echo ""
echo "或运行 CLI 应用："
echo "  python3 src/main.py --help"
echo ""
