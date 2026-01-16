#!/usr/bin/env python3
"""
诊断打包后的可执行文件问题
"""
import sys
import os
import subprocess
from pathlib import Path


def check_pyinstaller():
    """检查 PyInstaller 是否正确安装"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller 版本: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("❌ PyInstaller 未安装")
        print("   请运行: pip install pyinstaller")
        return False


def check_source_files():
    """检查源文件是否存在"""
    print("\n【检查源文件】")

    files = [
        ("src/gui/main.py", "GUI 入口"),
        ("src/main.py", "CLI 入口"),
        ("src/core/sync_service.py", "同步服务"),
        ("src/gui/main_window.py", "主窗口"),
    ]

    all_exist = True
    for file_path, description in files:
        if Path(file_path).exists():
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ {description}: {file_path} (不存在)")
            all_exist = False

    return all_exist


def check_config_file():
    """检查配置文件"""
    print("\n【检查配置文件】")

    if Path("users.json").exists():
        print("✅ users.json 存在")
        try:
            import json
            with open("users.json", "r") as f:
                data = json.load(f)
                user_count = len(data.get("users", []))
                print(f"   配置了 {user_count} 个用户")
        except Exception as e:
            print(f"⚠️  users.json 格式错误: {e}")
    else:
        print("⚠️  users.json 不存在（首次运行时会自动创建）")

    return True


def check_dependencies():
    """检查依赖"""
    print("\n【检查依赖】")

    # 检查核心依赖
    core_deps = [
        ("requests", "requests"),
        ("garmin", "garmin"),
        ("xiaomi", "xiaomi"),
        ("fit_tool", "fit-tool"),
    ]

    for module, package in core_deps:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} 未安装")
            print(f"   安装命令: pip install {package}")

    # 检查 GUI 依赖
    try:
        import PyQt6
        print(f"✅ PyQt6 (GUI 可用)")
    except ImportError:
        print(f"⚠️  PyQt6 未安装 (GUI 版本需要)")


def check_dist_output():
    """检查 dist 目录"""
    print("\n【检查打包输出】")

    if Path("dist").exists():
        files = list(Path("dist").glob("*"))
        if files:
            print(f"找到 {len(files)} 个文件:")
            for f in files:
                size = f"{f.stat().st_size / 1024 / 1024:.1f} MB"
                print(f"  - {f.name} ({size})")
        else:
            print("❌ dist 目录为空")
    else:
        print("❌ dist 目录不存在")
        print("   请先运行打包: python build.py")


def test_executable():
    """测试可执行文件"""
    print("\n【测试可执行文件】")

    platform = sys.platform

    if platform == "win32":
        exe_files = list(Path("dist").glob("*.exe"))
        if exe_files:
            exe = exe_files[0]
            print(f"找到可执行文件: {exe}")
            print()
            print("尝试运行...")
            try:
                subprocess.run([str(exe), "--help"],
                              capture_output=True,
                              timeout=5,
                              check=False)
                print("✅ 可执行文件可以启动")
            except Exception as e:
                print(f"❌ 运行失败: {e}")
                print("\n可能的原因:")
                print("  1. 缺少运行时依赖")
                print("  2. 路径问题")
                print("  3. 权限问题")
        else:
            print("❌ 未找到 .exe 文件")

    elif platform == "darwin":
        executables = list(Path("dist").glob("GarminWeightSync"))
        executables.extend(list(Path("dist").glob("garmin-sync-cli")))

        if executables:
            exe = executables[0]
            print(f"找到可执行文件: {exe}")
            print()

            # 检查是否可执行
            if os.access(exe, os.X_OK):
                print("✅ 文件有执行权限")
            else:
                print("❌ 文件没有执行权限")
                print(f"   运行: chmod +x {exe}")

            # 检查 macOS 隔离属性
            try:
                result = subprocess.run(["xattr", "-l", str(exe)],
                                          capture_output=True,
                                          text=True)
                if "com.apple.quarantine" in result.stdout:
                    print("⚠️  文件被 macOS 隔离")
                    print(f"   解除命令: xattr -cr {exe}")
            except FileNotFoundError:
                print("⚠️  xattr 命令不可用（可能需要安装 xattr）")
        else:
            print("❌ 未找到可执行文件")

    else:  # Linux
        executables = list(Path("dist").glob("GarminWeightSync"))
        executables.extend(list(Path("dist").glob("garmin-sync-cli")))

        if executables:
            exe = executables[0]
            print(f"找到可执行文件: {exe}")

            if os.access(exe, os.X_OK):
                print("✅ 文件有执行权限")
            else:
                print("❌ 文件没有执行权限")
                print(f"   运行: chmod +x {exe}")
        else:
            print("❌ 未找到可执行文件")


def suggest_solutions():
    """建议解决方案"""
    print("\n" + "=" * 60)
    print("【常见问题解决方案】")
    print("=" * 60)

    print("\n1. 如果可执行文件无法启动:")
    print("   - Windows: 右键 -> 以管理员身份运行")
    print("   - macOS: 运行 xattr -cr dist/GarminWeightSync")
    print("   - Linux: chmod +x dist/GarminWeightSync")

    print("\n2. 如果提示缺少配置文件:")
    print("   - 将 users.json 复制到可执行文件同一目录")
    print("   - 或在可执行文件所在目录运行（会自动创建模板）")

    print("\n3. 如果启动后立即关闭:")
    print("   - 检查是否缺少 users.json")
    print("   - 在命令行运行查看错误信息:")
    print("     Windows: dist\\GarminWeightSync.exe")
    print("     macOS/Linux: ./dist/GarminWeightSync")

    print("\n4. 如果显示 DLL/so 缺失:")
    print("   - 重新打包，确保使用了虚拟环境")
    print("   - 或使用 --debug 模式打包查看详细日志")

    print("\n5. 完全重新打包:")
    print("   rm -rf build dist")
    print("   python build.py")


def main():
    """主函数"""
    print("=" * 60)
    print("Garmin Weight Sync - 打包诊断工具")
    print("=" * 60)

    # 1. 检查 PyInstaller
    if not check_pyinstaller():
        return

    # 2. 检查源文件
    if not check_source_files():
        print("\n❌ 源文件不完整，请确保在项目根目录运行")
        return

    # 3. 检查依赖
    check_dependencies()

    # 4. 检查配置文件
    check_config_file()

    # 5. 检查 dist 输出
    check_dist_output()

    # 6. 测试可执行文件
    if Path("dist").exists():
        test_executable()

    # 7. 提供解决方案
    suggest_solutions()

    print("\n" + "=" * 60)
    print("诊断完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
