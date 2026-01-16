#!/usr/bin/env python3
"""
检查项目环境状态
"""
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    print(f"Python 版本: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("⚠️  警告: 建议使用 Python 3.8 或更高版本")
        return False
    else:
        print("✅ Python 版本符合要求")
        return True

def check_module(module_name, package_name=None):
    """检查模块是否已安装"""
    if package_name is None:
        package_name = module_name

    try:
        __import__(module_name)
        print(f"✅ {module_name} 已安装")
        return True
    except ImportError:
        print(f"❌ {module_name} 未安装")
        print(f"   安装命令: pip install {package_name}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("Garmin 体重同步管理 - 环境检查")
    print("=" * 60)
    print()

    all_ok = True

    # 1. 检查 Python 版本
    print("【1. Python 版本检查】")
    if not check_python_version():
        all_ok = False
    print()

    # 2. 检查核心依赖
    print("【2. 核心依赖检查】")
    core_modules = [
        ("requests", "requests"),
        ("cryptography", "cryptography"),
        ("fit_tool", "fit-tool"),
        ("garth", "garth"),
        ("pydantic", "pydantic"),
    ]

    for module, package in core_modules:
        if not check_module(module, package):
            all_ok = False
    print()

    # 3. 检查 GUI 依赖
    print("【3. GUI 依赖检查】")
    gui_modules = [
        ("PyQt6", "PyQt6"),
    ]

    has_gui = True
    for module, package in gui_modules:
        if not check_module(module, package):
            has_gui = False

    if not has_gui:
        print()
        print("ℹ️  GUI 功能需要 PyQt6，但 CLI 功能不受影响")
        print("   安装命令: pip install PyQt6")
    print()

    # 4. 检查项目文件
    print("【4. 项目文件检查】")
    required_files = [
        ("src/core/sync_service.py", "应用层"),
        ("src/gui/main.py", "GUI 程序"),
        ("src/main.py", "CLI 程序"),
        ("users.json", "配置文件（可选）"),
    ]

    for file_path, description in required_files:
        if Path(file_path).exists():
            print(f"✅ {description} ({file_path})")
        else:
            print(f"⚠️  {description} 不存在 ({file_path})")
    print()

    # 5. 总结
    print("=" * 60)
    if all_ok:
        print("✅ 所有核心依赖已安装，可以使用 CLI 功能")
        print()
        print("🚀 启动方式:")
        print("   CLI: python src/main.py --config users.json --sync")
        if has_gui:
            print("   GUI: python src/gui/main.py")
        else:
            print("   GUI: 需要先安装 PyQt6 (pip install PyQt6)")
    else:
        print("❌ 缺少核心依赖，请先安装:")
        print("   pip install -r requirements.txt")
        print()
        print("然后重新运行此脚本检查")

    print("=" * 60)
    print()

if __name__ == "__main__":
    main()
