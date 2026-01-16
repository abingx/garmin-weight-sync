# Garmin 体重同步管理 - GUI 版本

## 桌面应用程序实现说明

我已经为您创建了完整的 PyQt6 桌面应用程序代码。以下是项目结构和使用说明。

### 📁 项目结构

```
garmin-weight-sync/
├── src/
│   ├── core/                    # ✅ 应用层（新增）
│   │   ├── __init__.py
│   │   ├── models.py            # 数据模型定义
│   │   ├── config_manager.py    # 增强的配置管理
│   │   └── sync_service.py      # 同步服务编排器
│   ├── gui/                     # ✅ GUI 层（新增）
│   │   ├── __init__.py
│   │   ├── main.py              # GUI 入口
│   │   └── main_window.py       # 主窗口
│   ├── main.py                  # CLI 入口（保留）
│   ├── xiaomi/                  # 保持不变
│   └── garmin/                  # 保持不变
├── requirements-gui.txt         # GUI 依赖
└── README_GUI.md               # 本文件
```

### ✨ 核心特性

1. **完整的应用层**
   - `SyncOrchestrator`: 统一同步接口，GUI 和 CLI 共用
   - `EnhancedConfigManager`: 增强的配置管理
   - `UserModel`, `SyncProgress`: 数据模型

2. **PyQt6 图形界面**
   - 用户列表显示
   - 实时同步进度
   - 日志输出窗口
   - 工具栏和菜单栏
   - 多线程同步（不阻塞界面）

3. **零代码破坏**
   - `src/xiaomi/` 和 `src/garmin/` 完全不动
   - CLI 功能完全保留
   - GUI 通过调用应用层实现

### 🚀 快速开始

#### 方式 1: 使用 GUI（推荐）

```bash
# 1. 安装依赖
pip install -r requirements-gui.txt

# 注意：PyQt6 需要 Qt 开发环境
# macOS: brew install qt@6
# Windows: 下载安装 Qt 6.x
# Linux: sudo apt-get install qt6-base-dev

# 2. 运行 GUI 应用
python src/gui/main.py
```

#### 方式 2: 使用 CLI（原有方式）

```bash
# CLI 功能完全保留
python src/main.py --config users.json --sync
```

### 📱 GUI 功能说明

#### 主窗口功能
- **用户列表**: 显示所有已配置用户及其状态
- **添加用户**: 通过表单添加新用户（开发中）
- **同步选中**: 同步选中的用户
- **全部同步**: 同步所有用户
- **刷新**: 重新加载用户列表
- **实时日志**: 显示同步进度和结果

#### 同步流程
1. 点击用户选择
2. 点击"同步选中用户"
3. 实时查看同步进度
4. 完成后显示汇总结果

### ⚠️ PyQt6 安装问题

PyQt6 需要 Qt 开发环境，安装可能遇到问题。以下是替代方案：

#### 方案 A: 使用虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 升级 pip
pip install --upgrade pip

# 安装 PyQt6
pip install PyQt6

# 运行 GUI
python src/gui/main.py
```

#### 方案 B: 预编译版本

如果 PyQt6 安装失败，可以：
1. 使用 CLI 版本（`python src/main.py --sync`）
2. 使用 Docker 版本（`docker-compose up -d web`）
3. 等待提供独立的 .exe/.app 可执行文件

### 🎯 已实现功能

✅ 应用层架构（`src/core/`）
✅ 数据模型定义
✅ 同步服务编排器
✅ 主窗口界面
✅ 用户列表加载
✅ 同步功能（多线程）
✅ 实时进度显示
✅ 日志输出

### 📋 待实现功能

⏳ 用户添加/编辑对话框
⏳ 小米登录向导
⏳ 设置对话框
⏳ 系统托盘支持
⏳ 定时任务配置
⏳ 数据过滤可视化编辑

### 🔧 开发说明

#### 代码架构

```
GUI 层（PyQt6）
    ↓ 调用
应用层（core/）
    ↓ 调用
业务逻辑层（xiaomi/、garmin/）
```

#### 关键文件

1. **`src/core/sync_service.py`**
   - `SyncOrchestrator`: 核心同步编排器
   - 提供统一接口供 GUI 和 CLI 调用
   - 支持进度回调（Generator 模式）

2. **`src/gui/main_window.py`**
   - `MainWindow`: 主窗口
   - `SyncWorker`: 后台同步线程
   - 信号槽机制更新 UI

3. **`src/gui/main.py`**
   - GUI 入口
   - 高 DPI 支持

### 🐛 常见问题

#### Q1: ImportError: No module named 'PyQt6'
**A**: 需要安装 PyQt6
```bash
pip install PyQt6
```

#### Q2: PyQt6 安装失败
**A**: 可能需要 Qt 开发环境
- macOS: `brew install qt@6`
- Ubuntu: `sudo apt-get install qt6-base-dev`
- 或使用虚拟环境

#### Q3: GUI 无法启动
**A**: 检查：
1. PyQt6 是否正确安装
2. 是否在正确的目录
3. 查看 Python 版本（建议 3.8+）

### 📊 下一步计划

1. 完善用户管理功能（添加/编辑对话框）
2. 实现小米登录向导
3. 添加设置页面
4. 实现系统托盘
5. 添加定时任务功能
6. 打包成独立可执行文件

### 📝 注意事项

- 当前版本是 **MVP（最小可行产品）**
- 核心同步功能已实现
- GUI 界面已可用
- 部分高级功能待开发

---

## 使用示例

### GUI 方式

```bash
# 启动 GUI
python src/gui/main.py

# 操作步骤：
# 1. 点击"刷新"加载用户列表
# 2. 选择要同步的用户
# 3. 点击"同步选中用户"
# 4. 查看实时日志和进度
# 5. 等待同步完成
```

### CLI 方式（保持兼容）

```bash
# 同步所有用户
python src/main.py --config users.json --sync

# 仅生成 FIT 文件
python src/main.py --config users.json --fit

# 查看最近 20 条数据
python src/main.py --config users.json --limit 20
```

---

**开发者**: Leslie
**版本**: 2.0 (GUI Beta)
**最后更新**: 2026-01-14
