# 📚 Garmin Weight Sync - 文档索引

## 🎯 快速导航

### 新手必读
1. **[QUICKSTART.md](QUICKSTART.md)** - 快速开始指南（推荐首先阅读）
2. **[STATUS.md](STATUS.md)** - 当前状态和功能列表
3. **[README.md](README.md)** - 项目说明（原 README）

### 打包分发
4. **[PACKAGING_GUIDE.md](PACKAGING_GUIDE.md)** - 完整打包指南
5. **[BUILD_GUIDE.md](BUILD_GUIDE.md)** - 详细打包说明
6. **[build.py](build.py)** - 交互式打包脚本

### 故障排除
7. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - 常见问题解决

### GUI 详细说明
8. **[README_GUI.md](README_GUI.md)** - GUI 功能详细说明

---

## 🚀 快速开始（3 步）

### 步骤 1: 配置用户
```bash
# 编辑 users.json 文件，添加账号信息
```

### 步骤 2: 获取小米 Token
```bash
python src/xiaomi/login.py --config users.json
```

### 步骤 3: 开始同步

**方式 A: GUI**
```bash
python src/gui/main.py
```

**方式 B: CLI**
```bash
python src/main.py --config users.json --sync
```

---

## 📦 打包成可执行文件（2 步）

### 步骤 1: 安装打包工具
```bash
pip install pyinstaller
```

### 步骤 2: 运行打包脚本
```bash
# Windows
build.bat

# Linux/macOS
./build.sh

# 或跨平台
python build.py
```

**输出**: `dist/` 目录下的可执行文件

---

## 📂 项目结构

```
garmin-weight-sync/
├── src/
│   ├── core/              # 应用层（新增）
│   │   ├── models.py
│   │   ├── config_manager.py
│   │   └── sync_service.py
│   ├── gui/               # GUI 层（新增）
│   │   ├── main.py
│   │   └── main_window.py
│   ├── main.py            # CLI 入口（保留）
│   ├── xiaomi/            # 小米模块（不变）
│   └── garmin/            # Garmin 模块（不变）
│
├── build.py              # 打包脚本
├── build.bat             # Windows 打包
├── build.sh              # Linux/macOS 打包
│
├── run_gui.py            # GUI 启动脚本
├── check_environment.py  # 环境检查
├── check_gui_deps.py     # GUI 依赖检查
│
├── requirements.txt       # 核心依赖
├── requirements-gui.txt   # GUI 依赖
│
├── users.json            # 配置文件
│
└── docs/                 # 文档（本目录）
    ├── QUICKSTART.md
    ├── STATUS.md
    ├── PACKAGING_GUIDE.md
    ├── BUILD_GUIDE.md
    ├── TROUBLESHOOTING.md
    └── README_GUI.md
```

---

## ✨ 功能特性

### 核心功能
- ✅ 小米体重数据获取
- ✅ Garmin 同步（分块上传，每批 500 条）
- ✅ 数据过滤支持
- ✅ 多用户管理
- ✅ CLI 和 GUI 双模式

### GUI 功能
- ✅ 图形化用户界面
- ✅ 实时同步进度
- ✅ 多线程处理
- ✅ 详细日志输出
- ✅ 用户列表管理
- ⏳ 用户添加/编辑对话框（待实现）
- ⏳ 小米登录向导（待实现）

### 高级功能
- ✅ 分块上传（避免超限）
- ✅ 失败重试（继续处理后续批次）
- ✅ 汇总统计
- ✅ 日志记录

---

## 🎓 使用场景

### 场景 1: 日常使用（推荐 GUI）
```bash
python src/gui/main.py
```
- 图形界面，操作简单
- 实时进度显示
- 适合非技术用户

### 场景 2: 自动化同步（推荐 CLI）
```bash
python src/main.py --config users.json --sync
```
- 适合脚本和定时任务
- 可以集成到其他系统
- Docker 友好

### 场景 3: 分发使用（推荐打包）
```bash
python build.py
```
- 独立可执行文件
- 用户无需安装 Python
- 跨平台支持

---

## 🔧 配置说明

### users.json 结构
```json
{
    "users": [
        {
            "username": "xiaomi_username",
            "password": "xiaomi_password",
            "model": "yunmai.scales.ms103",
            "token": {...},
            "garmin": {
                "email": "garmin_email",
                "password": "garmin_password",
                "domain": "CN"  // or "COM"
            }
        }
    ]
}
```

### 过滤配置（可选）
```json
"garmin": {
    "filter": {
        "enabled": true,
        "conditions": [
            {"field": "Weight", "operator": "between", "value": [60, 70]}
        ],
        "logic": "and"
    }
}
```

---

## 📊 版本历史

### v2.0 (当前版本)
- ✨ 新增 GUI 图形界面
- ✨ 新增应用层架构
- ✨ 分块上传优化（500条/批）
- ✨ 完整的打包支持
- ✅ CLI 完全兼容

### v1.0
- 基础 CLI 功能
- 小米和 Garmin 集成

---

## 💡 提示

1. **首次使用**需要先运行 `src/xiaomi/login.py` 获取 Token
2. **配置文件** `users.json` 需要手动创建或自动生成
3. **打包** 前确保所有依赖已安装
4. **可执行文件** 需要和 `users.json` 在同一目录

---

## 📞 获取帮助

- 查看对应的文档
- 提交 Issue 到 GitHub
- 查看错误日志

---

**开发者**: Leslie
**许可**: MIT License
**最后更新**: 2026-01-14
