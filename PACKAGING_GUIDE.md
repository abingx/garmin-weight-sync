# 🎉 Garmin Weight Sync - 完整使用指南

## 📦 如何打包成可执行软件

### 方法 1: 使用交互式打包脚本（推荐）

```bash
# Windows
build.bat

# Linux/macOS
./build.sh

# 或跨平台（需要先安装 pyinstaller）
python build.py
```

然后选择：
- **选项 1**: GUI 版本（有图形界面）
- **选项 2**: CLI 版本（命令行，更小）
- **选项 3**: 全部打包

### 方法 2: 手动打包

```bash
# 1. 安装 PyInstaller
pip install pyinstaller

# 2. GUI 版本
pyinstaller --name=GarminWeightSync --windowed --onefile src/gui/main.py

# 3. CLI 版本
pyinstaller --name=garmin-sync-cli --onefile src/main.py
```

---

## 📂 打包后的文件

打包完成后，在 `dist/` 目录会看到：

### Windows
```
dist/
├── GarminWeightSync.exe      # GUI 版本
└── garmin-sync-cli.exe        # CLI 版本
```

### macOS
```
dist/
├── GarminWeightSync           # GUI 版本（可执行文件）
└── garmin-sync-cli            # CLI 版本
```

### Linux
```
dist/
├── GarminWeightSync           # GUI 版本
└── garmin-sync-cli            # CLI 版本
```

---

## 🚀 使用可执行文件

### Windows
1. 双击 `GarminWeightSync.exe`
2. 或在命令行运行: `GarminWeightSync.exe`

### macOS
1. 双击 `GarminWeightSync`
2. 或在终端运行: `./dist/GarminWeightSync`
3. 如果提示"已损坏"，运行: `xattr -cr dist/GarminWeightSync`

### Linux
```bash
./dist/GarminWeightSync
```

---

## ⚙️ 配置文件说明

可执行文件需要 `users.json` 配置文件在同一目录：

### 项目目录结构
```
garmin-weight-sync/
├── GarminWeightSync.exe      # 可执行文件
├── users.json                # 配置文件
└── data/                     # 数据目录（自动生成）
    ├── .garth/               # Garmin 会话
    └── garmin-fit/           # FIT 文件
```

### 配置文件模板

如果 `users.json` 不存在，首次运行会自动创建模板。

或手动创建：
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

---

## 🔧 首次使用步骤

### 1. 获取小米 Token（必需）

**Windows:**
```bash
garmin-sync-cli.exe --config users.json
```
然后按提示完成小米登录

**macOS/Linux:**
```bash
./garmin-sync-cli --config users.json
```

或使用原始 Python 脚本：
```bash
python src/xiaomi/login.py --config users.json
```

### 2. 编辑配置文件

打开 `users.json`，填写：
- 小米账号信息
- Garmin 账号信息

### 3. 运行同步

**GUI 方式:**
- 双击 `GarminWeightSync.exe`
- 点击"同步选中用户"或"全部同步"

**CLI 方式:**
```bash
# Windows
garmin-sync-cli.exe --config users.json --sync

# macOS/Linux
./garmin-sync-cli --config users.json --sync
```

---

## 📊 文件大小

| 版本 | 大小 | 说明 |
|------|------|------|
| CLI 版本 | ~30-50 MB | 轻量，命令行操作 |
| GUI 版本 | ~100-150 MB | 图形界面，易用 |

**推荐**:
- 个人使用: GUI 版本（更友好）
- 服务器/Docker: CLI 版本（更轻量）

---

## ⚠️ 常见问题

### Q1: 打包后双击没反应
**A**:
1. 右键 -> "以管理员身份运行"
2. 或在命令行运行查看错误信息

### Q2: macOS 提示"已损坏"
**A**:
```bash
xattr -cr dist/GarminWeightSync
```

### Q3: Windows Defender 报病毒
**A**: 这是误报，添加到排除列表即可

### Q4: 缺少配置文件
**A**:
1. 将 `users.json` 放在可执行文件同一目录
2. 或首次运行会自动创建模板

### Q5: PyQt6 相关错误
**A**:
- 使用 CLI 版本（不需要 PyQt6）
- 或确保打包时使用了虚拟环境

---

## 🎯 完整工作流程

### 开发环境
```bash
# 1. 开发和测试
python src/gui/main.py          # GUI
python src/main.py --sync       # CLI
```

### 打包分发
```bash
# 2. 打包
python build.py

# 3. 测试可执行文件
dist/GarminWeightSync

# 4. 分发给用户
# - 上传到 GitHub Releases
# - 发送文件给用户
# - 创建安装程序
```

### 用户使用
```bash
# 1. 下载并解压
# 2. 配置 users.json
# 3. 运行可执行文件
# 4. 完成！
```

---

## 📦 打包优化建议

### 减小文件大小

如果需要更小的文件：

1. **只打包 CLI 版本** (~30MB)
2. **使用 UPX 压缩**（可减少 30-50%）
3. **排除不需要的模块**（已优化）

### 增强用户体验

1. **添加图标**（参考 `src/gui/resources/icons/README.md`）
2. **创建安装程序**（NSIS, Inno Setup, etc.）
3. **代码签名**（避免安全警告）

---

## 🎉 完成！

现在您已经有了：
- ✅ 完整的 GUI 桌面应用
- ✅ 打包成独立可执行文件
- ✅ 跨平台支持（Windows/macOS/Linux）
- ✅ 详细的文档和指南

---

## 📞 需要帮助？

- 查看 `BUILD_GUIDE.md` 了解详细打包步骤
- 查看 `TROUBLESHOOTING.md` 解决常见问题
- 查看 `QUICKSTART.md` 了解使用方法

---

**版本**: 2.0
**最后更新**: 2026-01-14
**开发者**: Leslie
