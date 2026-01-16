# Garmin 体重同步管理 - 快速开始指南

## ✅ 已实现功能

### 1. 核心应用层（100% 完成）
- ✅ 数据模型（`src/core/models.py`）
- ✅ 增强配置管理（`src/core/config_manager.py`）
- ✅ 同步服务编排器（`src/core/sync_service.py`）

### 2. PyQt6 图形界面（80% 完成）
- ✅ 主窗口框架
- ✅ 用户列表加载
- ✅ 同步功能（多线程）
- ✅ 实时进度显示
- ✅ 日志输出窗口
- ✅ 工具栏和菜单栏
- ⏳ 用户添加/编辑对话框（待实现）
- ⏳ 小米登录向导（待实现）
- ⏳ 设置对话框（待实现）

### 3. CLI 兼容性（100% 保留）
- ✅ 所有原有命令行功能保持不变
- ✅ 通过应用层调用业务逻辑

---

## 🚀 使用方法

### 方式 A: GUI 图形界面（推荐）

```bash
# 方式 1: 使用启动脚本（最简单）
python run_gui.py

# 方式 2: 直接运行
python src/gui/main.py

# 方式 3: 从项目根目录运行
cd /path/to/garmin-weight-sync
python src/gui/main.py
```

**GUI 功能说明：**
1. 用户列表：显示所有已配置用户
2. 同步选中：点击"同步选中用户"按钮
3. 全部同步：点击"全部同步"按钮
4. 实时日志：查看同步进度和结果
5. 自动保存：同步完成自动更新配置文件

### 方式 B: CLI 命令行（原有方式）

```bash
# 同步所有用户到 Garmin
python src/main.py --config users.json --sync

# 仅生成 FIT 文件，不上传
python src/main.py --config users.json --fit

# 查看最近 20 条体重数据
python src/main.py --config users.json --limit 20

# 指定 FIT 文件输出目录
python src/main.py --config users.json --fit --output-dir ./my_fit_files
```

---

## 📋 配置文件说明

配置文件：`users.json`

```json
{
    "users": [
        {
            "username": "your_xiaomi_username",
            "password": "your_xiaomi_password",
            "model": "yunmai.scales.ms103",
            "token": {
                "userId": "",
                "passToken": "",
                "ssecurity": ""
            },
            "garmin": {
                "email": "your_garmin_email",
                "password": "your_garmin_password",
                "domain": "CN"
            }
        }
    ]
}
```

**首次使用**需要先获取小米 Token：
```bash
python src/xiaomi/login.py --config users.json
```

---

## 🔧 安装说明

### 基础依赖
```bash
pip install -r requirements.txt
```

### GUI 依赖（可选）
```bash
pip install -r requirements-gui.txt
```

**注意**：PyQt6 安装可能需要 Qt 开发环境：
- **macOS**: `brew install qt@6`
- **Ubuntu**: `sudo apt-get install qt6-base-dev`
- **Windows**: 下载安装 Qt 6.x

如果 PyQt6 安装失败，可以使用 CLI 版本。

---

## 💡 使用技巧

### 1. 分块上传
系统自动将数据分成 500 条一批，避免上传失败。

### 2. 失败重试
如果某个批次失败，其他批次仍会继续上传。最后会显示汇总结果。

### 3. 多用户管理
支持在 `users.json` 中配置多个用户，GUI 可以分别同步。

### 4. 定时同步
可以使用系统定时任务定期运行：
```bash
# macOS/Linux (crontab)
0 2 * * * cd /path/to/garmin-weight-sync && python src/main.py --sync

# Windows (任务计划程序)
# 创建基本任务，程序: python，参数: src/main.py --sync
```

---

## 🐛 常见问题

### Q1: PyQt6 安装失败怎么办？
**A**: 使用 CLI 版本即可，功能完全一样。

### Q2: 如何添加新用户？
**A**:
1. 方式 1: 手动编辑 `users.json`
2. 方式 2: 使用 GUI 的"添加用户"按钮（待完善）

### Q3: 同步失败怎么办？
**A**:
1. 检查网络连接
2. 检查小米 Token 是否过期（重新运行 login.py）
3. 检查 Garmin 账号密码是否正确
4. 查看日志获取详细错误信息

### Q4: 如何查看同步历史？
**A**:
- GUI 方式：查看日志窗口
- CLI 方式：查看终端输出
- 生成的 FIT 文件在 `data/garmin-fit/` 目录

---

## 📊 项目结构

```
garmin-weight-sync/
├── src/
│   ├── core/               # 应用层（新增）
│   │   ├── models.py       # 数据模型
│   │   ├── config_manager.py  # 配置管理
│   │   └── sync_service.py # 同步编排器
│   ├── gui/                # GUI 层（新增）
│   │   ├── main.py         # GUI 入口
│   │   └── main_window.py  # 主窗口
│   ├── main.py             # CLI 入口（保留）
│   ├── xiaomi/             # 小米模块（不变）
│   └── garmin/             # Garmin 模块（不变）
├── run_gui.py             # GUI 启动脚本
├── requirements.txt        # 基础依赖
├── requirements-gui.txt    # GUI 依赖
├── users.json             # 配置文件
└── README_GUI.md          # GUI 详细文档
```

---

## 🎯 下一步计划

### 短期（1-2 周）
- [ ] 实现用户添加/编辑对话框
- [ ] 实现小米登录向导（内嵌验证码）
- [ ] 实现设置对话框

### 中期（3-4 周）
- [ ] 系统托盘支持
- [ ] 定时任务配置界面
- [ ] 数据过滤可视化编辑

### 长期（1-2 月）
- [ ] 打包成独立可执行文件
- [ ] 支持多语言（i18n）
- [ ] 体重数据图表显示

---

## 📞 支持

- **Issues**: https://github.com/XiaoSiHwang/garmin-weight-sync/issues
- **文档**: 查看 README_GUI.md
- **开发者**: Leslie

---

**版本**: 2.0 (GUI Beta)
**最后更新**: 2026-01-14
**许可**: MIT License
