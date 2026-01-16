# Garmin Weight Sync 打包指南

## 📦 打包成可执行文件

本指南将帮助您将 Garmin Weight Sync 打包成独立的可执行文件（.exe/.app），无需安装 Python 即可运行。

---

## 🚀 快速开始

### 1. 安装打包工具

```bash
pip install pyinstaller
```

### 2. 运行打包脚本

```bash
python build.py
```

然后选择要打包的版本：
- **选项 1**: GUI 版本（推荐，有图形界面）
- **选项 2**: CLI 版本（命令行，更轻量）
- **选项 3**: 全部打包

### 3. 查看输出

打包完成后，可执行文件在 `dist/` 目录：
- Windows: `dist/GarminWeightSync.exe` 或 `dist/garmin-sync-cli.exe`
- macOS: `dist/GarminWeightSync` 或 `dist/garmin-sync-cli`
- Linux: `dist/GarminWeightSync` 或 `dist/garmin-sync-cli`

---

## 📋 详细步骤

### Windows 打包

```bash
# 1. 安装 PyInstaller
pip install pyinstaller

# 2. 运行打包脚本
python build.py

# 选择选项 1 (GUI) 或 2 (CLI)

# 3. 等待打包完成（可能需要几分钟）

# 4. 测试可执行文件
dist\GarminWeightSync.exe
```

### macOS 打包

```bash
# 1. 安装 PyInstaller
pip install pyinstaller

# 2. 运行打包脚本
python build.py

# 3. 如果需要创建 .app 包
# 编辑 build.py，取消注释 macOS 相关配置

# 4. 测试可执行文件
./dist/GarminWeightSync
```

### Linux 打包

```bash
# 1. 安装 PyInstaller
pip install pyinstaller

# 2. 运行打包脚本
python build.py

# 3. 测试可执行文件
./dist/GarminWeightSync
```

---

## 🔧 高级配置

### 自定义图标

1. 准备图标文件：
   - Windows: `.ico` 文件 (256x256)
   - macOS: `.icns` 文件
   - Linux: `.png` 文件 (256x256)

2. 将图标放到 `src/gui/resources/icons/` 目录

3. 修改 `build.py` 中的图标路径

### 减小文件大小

当前打包配置已优化，排除了不需要的模块（tkinter, matplotlib, numpy 等）。

如果还需要进一步减小：
1. 使用 `--strip` 选项（移除调试符号）
2. 使用 UPX 压缩（需要额外安装）

### 单文件 vs 目录模式

- **单文件模式** (`--onefile`): 所有内容打包成一个文件，体积较大但便于分发
- **目录模式** (移除 `--onefile`): 打包成一个目录，体积较小但文件较多

当前默认使用单文件模式。

---

## ⚠️ 常见问题

### Q1: PyInstaller 安装失败

**A**: 使用虚拟环境
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install pyinstaller
```

### Q2: 打包后运行报错

**A**:
1. 检查是否所有依赖都已安装
2. 查看 PyInstaller 的警告信息
3. 尝试在控制台运行查看错误详情

### Q3: macOS 提示"已损坏"

**A**: 这是 macOS 的安全机制，需要解除隔离：
```bash
xattr -cr dist/GarminWeightSync
```

### Q4: Windows Defender 报病毒

**A**: 误报，添加到排除列表即可。PyInstaller 打包的程序经常被误报。

### Q5: 文件太大（>100MB）

**A**: 这是正常的，因为包含了：
- Python 运行时
- PyQt6 库（~50MB）
- 其他依赖库

如果需要更小的文件，可以考虑：
1. 只打包 CLI 版本（~30MB）
2. 使用目录模式（可以共享一些库文件）

---

## 📊 文件大小参考

- **CLI 版本**: 约 30-50 MB
- **GUI 版本**: 约 100-150 MB
  - 包含 PyQt6 (~50MB)
  - 包含其他依赖

---

## 🎯 打包最佳实践

1. **在虚拟环境中打包**
   ```bash
   python -m venv build_env
   source build_env/bin/activate
   pip install -r requirements-gui.txt
   pip install pyinstaller
   python build.py
   ```

2. **先在开发环境测试**
   ```bash
   python src/gui/main.py
   ```

3. **检查打包结果**
   ```bash
   # 查看包含的文件
   dist/GarminWeightSync
   ```

4. **在不同系统上测试**
   - 在没有 Python 的系统上测试
   - 检查所有功能是否正常

---

## 📦 分发可执行文件

### Windows
- 直接分发 `GarminWeightSync.exe`
- 可以创建安装程序（NSIS, Inno Setup）

### macOS
- 分发 `GarminWeightSync` 可执行文件
- 可以创建 .dmg 镜像
- 或者签名并公证（Apple Developer 账号）

### Linux
- 分发可执行文件
- 创建 .deb 或 .rpm 包
- 或使用 AppImage

---

## 🔄 自动化打包（可选）

### GitHub Actions

创建 `.github/workflows/build.yml`:

```yaml
name: Build

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]

    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install -r requirements-gui.txt
        pip install pyinstaller

    - name: Build
      run: python build.py

    - name: Upload artifact
      uses: actions/upload-artifact@v2
      with:
        name: garmin-sync-${{ matrix.os }}
        path: dist/
```

---

## ✅ 打包后验证

打包完成后，请验证：

1. **启动测试**
   ```bash
   # 双击运行
   GarminWeightSync
   ```

2. **功能测试**
   - 能否加载用户列表
   - 能否执行同步
   - 进度显示是否正常

3. **无依赖测试**
   - 在没有 Python 的系统上测试
   - 检查是否能独立运行

---

## 📞 需要帮助？

如果打包遇到问题：

1. 查看 PyInstaller 官方文档: https://pyinstaller.org/
2. 查看 `TROUBLESHOOTING.md`
3. 提交 Issue 到 GitHub

---

**最后更新**: 2026-01-14
**版本**: 2.0
