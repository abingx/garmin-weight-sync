#!/usr/bin/env python3
"""
检查并安装 GUI 依赖
"""
import subprocess
import sys

def check_pyqt6():
    """检查 PyQt6 是否安装"""
    try:
        import PyQt6
        return True
    except ImportError:
        return False

def install_pyqt6():
    """安装 PyQt6"""
    print("🔧 正在安装 PyQt6...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6"])
        print("✅ PyQt6 安装成功！")
        return True
    except subprocess.CalledProcessError:
        print("❌ PyQt6 自动安装失败")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("Garmin 体重同步管理 - GUI 依赖检查")
    print("=" * 60)
    print()

    # 检查 PyQt6
    if check_pyqt6():
        print("✅ PyQt6 已安装")
        print()
        print("🚀 您可以运行以下命令启动 GUI：")
        print("   python src/gui/main.py")
        print("   或")
        print("   python run_gui.py")
        return 0
    else:
        print("❌ PyQt6 未安装")
        print()

        response = input("是否要自动安装 PyQt6? (y/n): ").strip().lower()

        if response == 'y':
            if install_pyqt6():
                print()
                print("✅ 安装完成！现在可以运行 GUI：")
                print("   python src/gui/main.py")
                return 0
            else:
                print()
                print("⚠️ 自动安装失败，请手动安装：")
                print()
                print("   pip install PyQt6")
                print()
                print("如果安装失败，可能需要安装 Qt 开发环境：")
                print("   macOS: brew install qt@6")
                print("   Ubuntu: sudo apt-get install qt6-base-dev")
                print("   Windows: 下载安装 Qt 6.x")
                print()
                print("或者使用 CLI 版本：")
                print("   python src/main.py --config users.json --sync")
                return 1
        else:
            print()
            print("⏭️ 跳过安装")
            print()
            print("如需使用 GUI，请手动安装 PyQt6：")
            print("   pip install PyQt6")
            print()
            print("或者使用 CLI 版本：")
            print("   python src/main.py --config users.json --sync")
            return 1

if __name__ == "__main__":
    sys.exit(main())
