# GUI 启动故障排除

## ✅ 语法错误已修复

刚才的语法错误已修复！现在可以正常导入 GUI 模块了。

---

## 🔧 PyQt6 未安装问题

### 快速修复

运行以下命令检查并安装依赖：

```bash
python check_gui_deps.py
```

这个脚本会：
1. 检查 PyQt6 是否已安装
2. 如果未安装，询问是否自动安装
3. 提供详细的安装说明

### 手动安装 PyQt6

```bash
pip install PyQt6
```

### 如果 PyQt6 安装失败

#### 原因
PyQt6 需要 Qt 开发环境支持。

#### 解决方案

**方案 A: 使用虚拟环境（推荐）**
```bash
# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate  # Windows

# 升级 pip
pip install --upgrade pip

# 安装 PyQt6
pip install PyQt6

# 运行 GUI
python src/gui/main.py
```

**方案 B: 使用 CLI 版本（最简单）**
```bash
# CLI 功能完全一样，只是没有图形界面
python src/main.py --config users.json --sync
```

**方案 C: 安装 Qt 开发环境**
- **macOS**:
  ```bash
  brew install qt@6
  ```
- **Ubuntu/Debian**:
  ```bash
  sudo apt-get update
  sudo apt-get install qt6-base-dev qt6-tools-dev
  ```
- **Windows**:
  1. 下载 Qt 6.x: https://www.qt.io/download-qt-installer
  2. 安装时选择 "MinGW" 或 "MSVC"
  3. 设置环境变量
  4. 重新安装 PyQt6

---

## 📋 完整使用流程

### 首次使用

1. **配置用户信息**
   ```bash
   # 编辑 users.json 文件，添加你的账号信息
   # 或者先获取小米 Token
   python src/xiaomi/login.py --config users.json
   ```

2. **安装依赖**
   ```bash
   # 基础依赖
   pip install -r requirements.txt

   # GUI 依赖（可选）
   pip install -r requirements-gui.txt
   ```

3. **启动应用**

   **方式 1: GUI（推荐）**
   ```bash
   python src/gui/main.py
   ```

   **方式 2: CLI**
   ```bash
   python src/main.py --config users.json --sync
   ```

---

## 🐛 常见错误及解决方法

### 错误 1: SyntaxError: invalid syntax
✅ **已修复** - 这是之前的 `__init__.py` 语法问题，已解决。

### 错误 2: ModuleNotFoundError: No module named 'PyQt6'
**原因**: PyQt6 未安装

**解决**:
```bash
pip install PyQt6
```

### 错误 3: sipbuild.pyproject.PyProjectOptionException
**原因**: Qt 开发环境未安装

**解决**:
- macOS: `brew install qt@6`
- Ubuntu: `sudo apt-get install qt6-base-dev`
- 或使用虚拟环境

### 错误 4: ImportError: cannot import name 'SyncOrchestrator'
**原因**: 模块路径问题

**解决**:
```bash
# 确保在项目根目录运行
cd /path/to/garmin-weight-sync
python src/gui/main.py
```

---

## ✅ 验证安装

运行以下命令验证：

```bash
# 1. 检查 Python 版本（建议 3.8+）
python --version

# 2. 检查基础依赖
python -c "import garmin; print('✅ Garmin 模块正常')"
python -c "import xiaomi; print('✅ Xiaomi 模块正常')"

# 3. 检查 GUI 依赖
python -c "import PyQt6; print('✅ PyQt6 已安装')"

# 4. 测试 GUI 导入
python -c "import sys; sys.path.append('src'); from core import SyncOrchestrator; print('✅ 核心模块正常')"
```

---

## 📞 需要帮助？

如果以上方法都无法解决问题，请：

1. 查看 `QUICKSTART.md` 获取详细说明
2. 使用 CLI 版本（功能完全相同）
3. 提交 Issue 到 GitHub
4. 检查错误日志获取详细错误信息

---

## 💡 临时方案

如果 PyQt6 实在无法安装，可以：

**使用 CLI 版本** - 功能完全一样，只是没有图形界面：

```bash
# 同步所有用户
python src/main.py --config users.json --sync

# 只生成 FIT 文件
python src/main.py --config users.json --fit

# 查看最近数据
python src/main.py --config users.json --limit 20
```

等后续提供打包好的独立可执行文件（.exe/.app），就不需要安装任何依赖了。
