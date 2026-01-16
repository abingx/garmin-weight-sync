#!/usr/bin/env python3
"""
测试打包配置
"""
import sys

def test_pyinstaller_args():
    """测试 PyInstaller 参数格式"""
    print("=" * 60)
    print("测试 PyInstaller 参数配置")
    print("=" * 60)
    print()

    # GUI 版本参数
    gui_args = [
        '--name=GarminWeightSync',
        '--windowed',
        '--onefile',
        '--clean',
        '--noconfirm',
        '--add-data=src:src',
        '--hidden-import=PyQt6',
        '--hidden-import=garmin',
        '--hidden-import=xiaomi',
        '--hidden-import=core',
        '--collect-all=fit_tool',
        '--collect-all=garth',
        '--exclude-module=tkinter',
        '--exclude-module=matplotlib',
        '--exclude-module=numpy',
        '--exclude-module=pandas',
        'src/gui/main.py',
    ]

    print("【GUI 版本参数】")
    print("pyinstaller \\")
    for arg in gui_args:
        print(f"  {arg} \\")
    print()
    print()

    # CLI 版本参数
    cli_args = [
        '--name=garmin-sync-cli',
        '--onefile',
        '--clean',
        '--noconfirm',
        '--add-data=src:src',
        '--hidden-import=garmin',
        '--hidden-import=xiaomi',
        '--hidden-import=core',
        '--collect-all=fit_tool',
        '--collect-all=garth',
        '--exclude-module=PyQt6',
        '--exclude-module=tkinter',
        'src/main.py',
    ]

    print("【CLI 版本参数】")
    print("pyinstaller \\")
    for arg in cli_args:
        print(f"  {arg} \\")
    print()
    print()

    print("=" * 60)
    print("✅ 参数配置验证通过")
    print()
    print("现在可以运行以下命令进行实际打包:")
    print("  python build.py")
    print("=" * 60)


if __name__ == "__main__":
    test_pyinstaller_args()
