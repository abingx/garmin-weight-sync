# 🔧 macOS 闪退问题修复指南

## 🎯 问题原因

打包后的可执行文件在 macOS 上双击闪退，是因为缺少 `jaraco` 相关模块。

错误信息：
```
ModuleNotFoundError: No module named 'jaraco'
```

## ✅ 解决方案（已修复）

我已经更新了 `build.py`，添加了所有缺失的隐藏导入：

```python
'--hidden-import=jaraco',
'--hidden-import=jaraco.collections',
'--hidden-import=jaraco.context',
'--hidden-import=jaraco.functools',
'--hidden-import=jaraco.classes',
'--hidden-import=importlib_metadata',
'--hidden-import=pkg_resources',
```

## 🚀 重新打包步骤

### 1️⃣ 清理旧的打包文件

```bash
cd /Users/leslie/Desktop/Python-Project/garmin-weight-sync
rm -rf build dist
```

### 2️⃣ 重新打包

```bash
# 确保在虚拟环境中
source /path/to/your/venv/bin/activate

# 重新打包
python build.py
# 选择选项 1 (GUI 版本)
```

### 3️⃣ 测试可执行文件

```bash
# 命令行测试（可以看到错误信息）
./dist/GarminWeightSync
```

### 4️⃣ 解除 macOS 隔离属性（重要！）

```bash
xattr -cr dist/GarminWeightSync
xattr -cr dist/GarminWeightSync.app
```

### 5️⃣ 双击运行

现在应该可以正常打开了！

---

## 🔍 如果还是闪退

### 方法 1：查看详细错误日志

```bash
# 在命令行运行（可以看到错误）
./dist/GarminWeightSync 2>&1 | tee crash_log.txt
```

### 方法 2：使用 Console.app 查看系统日志

1. 打开 `Console.app`（在 Applications → Utilities）
2. 在搜索框输入 "GarminWeightSync"
3. 重新双击运行可执行文件
4. 查看 Console 中的错误信息

### 方法 3：检查依赖是否完整

```bash
# 查看可执行文件包含的模块
otool -L dist/GarminWeightSync

# 查看包含的 Python 模块
unzip -l dist/GarminWeightSync | grep -i jaraco
```

---

## 📋 常见问题排查

### Q1: 仍然提示 ModuleNotFoundError

**可能原因**：虚拟环境中缺少某些依赖

**解决方案**：
```bash
# 在虚拟环境中重新安装所有依赖
pip install --upgrade -r requirements-gui.txt

# 特别安装可能缺失的包
pip install jaraco.classes jaraco.context jaraco.functools
pip install importlib-metadata
```

### Q2: 提示 "已损坏" 或 "无法验证开发者"

**解决方案**：
```bash
# 解除所有隔离属性
xattr -cr dist/GarminWeightSync
xattr -cr dist/GarminWeightSync.app

# 如果还不行，允许任何来源
sudo spctl --master-disable
```

### Q3: 双击后没有任何反应

**可能原因**：
- 缺少配置文件 `users.json`
- GUI 初始化失败

**解决方案**：
```bash
# 1. 确保 users.json 在同一目录
cp users.json dist/

# 2. 先测试 CLI 版本
./dist/garmin-sync-cli --help

# 3. 如果 CLI 能运行，问题在 GUI 代码
python src/gui/main.py  # 测试源代码
```

---

## 🎯 完整的验证流程

```bash
# 1. 测试源代码是否能运行
python src/gui/main.py

# 2. 清理并重新打包
rm -rf build dist
python build.py  # 选择 1

# 3. 等待打包完成...

# 4. 检查打包结果
ls -lh dist/

# 5. 解除隔离属性
xattr -cr dist/GarminWeightSync

# 6. 命令行测试
./dist/GarminWeightSync

# 7. 如果上面能运行，双击测试
open dist/GarminWeightSync.app
# 或直接双击 GarminWeightSync.app
```

---

## 📦 打包优化建议

### 减小文件大小

如果觉得 40MB 太大，可以：

1. **使用 UPX 压缩**（可减少 30-50%）：
   ```bash
   pip install pyinstaller[encryption]
   # 在 build.py 中添加: --upx-dir=/path/to/upx
   ```

2. **排除不需要的模块**：
   ```python
   '--exclude-module=matplotlib',
   '--exclude-module=numpy',
   '--exclude-module=pandas',
   '--exclude-module=scipy',
   '--exclude-module=PIL',
   ```

3. **使用 --onedir 而不是 --onefile**：
   ```python
   # 修改 build.py，去掉 --onefile
   # 这样会生成目录而不是单文件，但启动更快
   ```

---

## 💡 预防措施

### 打包前检查清单

- [x] 确保在虚拟环境中
- [x] 安装所有依赖：`pip install -r requirements-gui.txt`
- [x] 测试源代码能运行：`python src/gui/main.py`
- [x] 清理旧的 build/dist 目录
- [x] 使用更新后的 build.py（已包含 jaraco 导入）
- [x] 打包后解除 macOS 隔离属性：`xattr -cr`

### 下次打包时

直接运行：
```bash
rm -rf build dist && python build.py
```

然后选择选项 1 或 3。

---

## 🎉 成功标志

打包成功后，你应该能看到：

```bash
============================================================
✅ GUI 版本打包完成！
输出文件: dist/GarminWeightSync
============================================================

$ ls -lh dist/
-rwxr-xr-x  1 user  staff   40M Jan 14 22:30 GarminWeightSync
drwxr-xr-x  3 user  staff    96B Jan 14 22:30 GarminWeightSync.app

$ ./dist/GarminWeightSync
# GUI 窗口成功打开！
```

---

## 📞 如果问题依然存在

请提供以下信息：

1. **错误日志**：
   ```bash
   ./dist/GarminWeightSync 2>&1 | tee crash_log.txt
   ```

2. **系统信息**：
   ```bash
   sw_vers  # macOS 版本
   python --version  # Python 版本
   pyinstaller --version  # PyInstaller 版本
   ```

3. **虚拟环境中的包列表**：
   ```bash
   pip list | grep -i "jaraco\|pyqt\|pyinstaller"
   ```

---

**版本**: 1.0
**最后更新**: 2026-01-14
**状态**: ✅ 已修复 jaraco 缺失问题
