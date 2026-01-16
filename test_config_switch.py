#!/usr/bin/env python3
"""
测试配置文件切换功能
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from core.sync_service import SyncOrchestrator

def test_reload_config():
    """测试配置重新加载功能"""
    print("=" * 60)
    print("测试配置文件切换功能")
    print("=" * 60)

    # 1. 使用默认配置初始化
    print("\n[1] 加载默认配置：users.json")
    orchestrator = SyncOrchestrator("users.json")
    users1 = orchestrator.list_users()
    print(f"✅ 用户数量：{len(users1)}")
    if users1:
        for user in users1:
            print(f"   - {user.username}")

    # 2. 切换到测试配置
    print("\n[2] 切换到测试配置：test_config.json")
    try:
        orchestrator.reload_config("test_config.json")
        users2 = orchestrator.list_users()
        print(f"✅ 用户数量：{len(users2)}")
        if users2:
            for user in users2:
                print(f"   - {user.username}")
    except Exception as e:
        print(f"❌ 切换配置失败：{e}")
        return False

    # 3. 切换回默认配置
    print("\n[3] 切换回默认配置：users.json")
    try:
        orchestrator.reload_config("users.json")
        users3 = orchestrator.list_users()
        print(f"✅ 用户数量：{len(users3)}")
        if users3:
            for user in users3:
                print(f"   - {user.username}")
    except Exception as e:
        print(f"❌ 切换配置失败：{e}")
        return False

    # 4. 测试不存在的配置
    print("\n[4] 测试不存在的配置：nonexistent.json")
    try:
        orchestrator.reload_config("nonexistent.json")
        print("❌ 应该抛出异常但没有")
        return False
    except Exception as e:
        print(f"✅ 正确抛出异常：{type(e).__name__}")

    print("\n" + "=" * 60)
    print("✅ 所有测试通过！")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_reload_config()
    sys.exit(0 if success else 1)
