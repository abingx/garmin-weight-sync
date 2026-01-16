# 🔧 macOS 打包后 [Errno 30] Read-only file system 修复说明

## 问题描述

**错误信息**：
```
[Errno 30] Read-only file system: 'data'
```

**原因**：
- 打包后的 macOS `.app` 应用程序包是只读文件系统
- 代码尝试在 `.app` 内部创建 `data` 目录
- 导致无法写入会话数据和 FIT 文件

**为什么命令行没问题？**
- 开发环境运行时，`data` 目录在项目根目录，可读可写
- 打包后，`data` 目录被 PyInstaller 打包进 `.app` 内部，变成只读

---

## ✅ 解决方案

### 核心思路
**不在应用内部创建 `data` 目录，而是在用户主目录创建数据目录，然后把路径传给 `GarminClient`**

### 修改的文件
1. ✅ **新增** `src/utils/paths.py` - 路径工具模块
2. ✅ **修改** `src/core/sync_service.py` - 使用可写路径
3. ✅ **修改** `src/core/config_manager.py` - 支持自定义数据目录
4. ✅ **修改** `src/gui/main_window.py` - 添加数据目录设置界面

**未修改的文件**：
- ✅ `src/garmin/client.py` - 保持原样
- ✅ `src/xiaomi/` - 完全不动

---

## 📂 数据目录位置

### macOS 打包后
```
~/Library/Application Support/GarminWeightSync/
├── .garth/
│   ├── user1@example.com/
│   │   └── session.json
│   └── user2@gmail.com/
│       └── session.json
└── garmin-fit/
    ├── weight_user1_20250115.fit
    └── weight_user2_20250115.fit
```

### Windows 打包后
```
%APPDATA%\GarminWeightSync\
├── .garth\
│   └── ...
└── garmin-fit\
    └── ...
```

### Linux 打包后
```
~/.local/share/GarminWeightSync/
├── .garth/
│   └── ...
└── garmin-fit/
    └── ...
```

### 开发环境（保持兼容）
```
项目根目录/data/
├── .garth/
│   └── ...
└── garmin-fit/
    └── ...
```

---

## 🎯 如何使用

### 方法 1：使用默认数据目录（推荐）

打包后的应用会自动使用系统标准位置：
- **macOS**: `~/Library/Application Support/GarminWeightSync`
- **Windows**: `%APPDATA%\GarminWeightSync`
- **Linux**: `~/.local/share/GarminWeightSync`

**无需任何配置**，应用会自动创建这些目录。

### 方法 2：自定义数据目录

1. 运行 GUI 应用
2. 点击工具栏的"📖 设置"按钮
3. 查看"当前数据目录"
4. 点击"自定义..."按钮选择自定义目录
5. 或点击"重置为默认"恢复默认目录

### 方法 3：通过配置文件设置

在 `users.json` 中添加 `settings` 节点：

```json
{
    "settings": {
        "data_dir": "/path/to/custom/data"
    },
    "users": [...]
}
```

---

## 🔄 重新打包

### 清理旧文件
```bash
rm -rf build dist
```

### 重新打包
```bash
python build.py
# 选择选项 1 (GUI 版本)
```

### 解除隔离属性（macOS）
```bash
xattr -cr dist/GarminWeightSync
xattr -cr dist/GarminWeightSync.app
```

---

## ✨ 新增功能

### GUI 设置界面

点击"📖 设置"按钮后会显示：

```
┌──────────────────────────────────────────────────────────┐
│ 数据目录设置                                    [×]      │
├──────────────────────────────────────────────────────────┤
│                                                            │
│ 当前数据目录：                                              │
│                                                            │
│ ~/Library/Application Support/GarminWeightSync            │
│                                                            │
│            [重置为默认]  [自定义...]  [关闭]              │
└──────────────────────────────────────────────────────────┘
```

- **重置为默认**：恢复使用系统标准数据目录
- **自定义...**：打开文件夹选择对话框，选择自定义目录
- **关闭**：关闭设置对话框

---

## 🔍 技术细节

### 路径计算逻辑

```python
def get_app_data_dir() -> Path:
    """自动检测运行环境并返回正确的数据目录"""

    if getattr(sys, 'frozen', False):
        # 打包后的应用
        if sys.platform == 'darwin':
            # macOS: ~/Library/Application Support/GarminWeightSync
            app_data = Path.home() / 'Library' / 'Application Support' / 'GarminWeightSync'
        elif sys.platform == 'win32':
            # Windows: %APPDATA%\GarminWeightSync
            app_data = Path(os.environ.get('APPDATA', ...)) / 'GarminWeightSync'
        else:
            # Linux: ~/.local/share/GarminWeightSync
            app_data = Path.home() / '.local' / 'share' / 'GarminWeightSync'
    else:
        # 开发环境：项目根目录/data
        app_data = project_root / 'data'

    app_data.mkdir(parents=True, exist_ok=True)
    return app_data
```

### GarminClient session_dir 传入

```python
# 在 sync_service.py 中创建 GarminClient 时：
session_dir = get_session_dir(
    email=user.garmin.email,
    custom_base=config_mgr.custom_data_dir  # 支持自定义路径
)

g_client = GarminClient(
    email=user.garmin.email,
    password=user.garmin.password,
    auth_domain=user.garmin.domain,
    session_dir=str(session_dir)  # 关键：传入可写路径
)
```

---

## 📊 修改对比

### 修改前（会导致错误）
```python
# garmin/client.py
def __init__(self, email, password, auth_domain="CN", session_dir="data/.garth"):
    self.session_dir = Path(session_dir) / email
    # 在打包后的 .app 中，data 目录是只读的！

# sync_service.py
g_client = GarminClient(
    email=user.garmin.email,
    password=user.garmin.password,
    auth_domain=user.garmin.domain
    # 使用默认的 session_dir="data/.garth"
)
```

### 修改后（正确）
```python
# sync_service.py
session_dir = get_session_dir(
    email=user.garmin.email,
    custom_base=None  # 使用默认系统路径
)
g_client = GarminClient(
    email=user.garmin.email,
    password=user.garmin.password,
    auth_domain=user.garmin.domain,
    session_dir=str(session_dir)  # 传入可写路径：~/Library/Application Support/...
)
```

---

## ✅ 验证修复

### 测试步骤

1. **重新打包应用**
   ```bash
   rm -rf build dist
   python build.py
   ```

2. **运行打包后的应用**
   ```bash
   open dist/GarminWeightSync.app
   # 或双击 GarminWeightSync.app
   ```

3. **执行同步操作**
   - 添加用户
   - 点击"同步"
   - 观察是否还有 `[Errno 30]` 错误

4. **检查数据目录**
   ```bash
   ls -la ~/Library/Application\ Support/GarminWeightSync/
   # 应该能看到 .garth 和 garmin-fit 目录
   ```

5. **测试自定义目录**
   - 点击"📖 设置"
   - 点击"自定义..."选择自定义目录
   - 再次同步，检查数据是否保存到自定义目录

---

## 🎉 成功标志

修复成功后，您应该看到：

```
$ ./dist/GarminWeightSync
# GUI 正常启动
# 点击"设置"，显示：当前数据目录：~/Library/Application Support/GarminWeightSync
# 点击"同步"，成功执行，没有 [Errno 30] 错误

$ ls ~/Library/Application\ Support/GarminWeightSync/
# 看到 .garth/ 和 garmin-fit/ 目录
```

---

## 📝 配置文件示例

### users.json（带自定义数据目录）
```json
{
    "settings": {
        "data_dir": "/Users/leslie/Custom/GarminData"
    },
    "users": [
        {
            "username": "user@example.com",
            "password": "...",
            "model": "yunmai.scales.ms103",
            "garmin": {
                "email": "user@garmin.com",
                "password": "...",
                "domain": "CN"
            }
        }
    ]
}
```

---

## 🔧 故障排除

### 问题 1：仍然出现 [Errno 30]
**解决**：
- 确认已清理旧的 build 和 dist 目录
- 重新打包
- 检查 `src/utils/paths.py` 是否存在

### 问题 2：设置目录后下次启动恢复默认
**解决**：
- 检查 `users.json` 是否有写入权限
- 确认配置文件包含 `settings.data_dir` 字段

### 问题 3：无法创建目录
**解决**：
- 检查用户主目录权限
- macOS：确保有 `~/Library/Application Support` 的写权限
- Windows：确保有 `%APPDATA%` 的写权限

---

## 📦 文件清单

### 新增文件
- ✅ `src/utils/__init__.py`
- ✅ `src/utils/paths.py`
- ✅ `DATA_DIR_FIX.md`（本文档）

### 修改文件
- ✅ `src/core/sync_service.py`
- ✅ `src/core/config_manager.py`
- ✅ `src/gui/main_window.py`

### 未修改文件（重要）
- ✅ `src/garmin/client.py` - 保持原样
- ✅ `src/xiaomi/*` - 完全不动
- ✅ `src/main.py` - CLI 不受影响

---

## 🚀 下一步

1. **在虚拟环境中重新打包**
   ```bash
   source venv/bin/activate
   rm -rf build dist
   python build.py
   ```

2. **测试打包后的应用**
   - 双击运行 `.app` 文件
   - 执行同步操作
   - 验证数据目录

3. **验证功能**
   - 检查数据是否保存到正确位置
   - 测试自定义数据目录功能
   - 确认不再出现 [Errno 30] 错误

---

**版本**: 1.0
**日期**: 2026-01-15
**状态**: ✅ 已实现，等待测试
**开发者**: Leslie
