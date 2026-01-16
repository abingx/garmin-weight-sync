#!/usr/bin/env python3
"""
GUI 应用启动脚本
"""
import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Check PyQt6
try:
    import PyQt6
    print("✅ PyQt6 已安装")
except ImportError:
    print("❌ PyQt6 未安装")
    print("\n请运行以下命令安装：")
    print("  pip install PyQt6")
    print("\n或使用虚拟环境：")
    print("  python3 -m venv .venv")
    print("  source .venv/bin/activate")
    print("  pip install PyQt6")
    sys.exit(1)

# Launch GUI
try:
    from gui.main import main
    print("🚀 启动 Garmin 体重同步管理 GUI...\n")
    main()
except Exception as e:
    print(f"\n❌ 启动失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
