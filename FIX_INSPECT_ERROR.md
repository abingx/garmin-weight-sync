# 🔧 修复 Pydantic/Logfire inspect.getsource 错误

## 🎯 问题原因

错误信息：
```
OSError: could not get source code
```

**根本原因**：
- `pydantic` 使用了 `logfire` 集成
- `logfire` 在初始化时会调用 `inspect.getsource()` 来获取源代码
- PyInstaller 打包后的代码是"冻结"的（frozen），没有源文件
- 因此 `inspect.getsource()` 抛出 `OSError`

## ✅ 解决方案

我已经创建了一个 **Runtime Hook** 来修复这个问题：

### pyi_rth_pyqt6.py

这个文件在程序启动时运行，做了以下修复：

1. **设置环境变量禁用 logfire 插件**：
   ```python
   os.environ['LOGFIRE_SKIP_PYDANTIC_PLUGIN'] = '1'
   os.environ['PYDANTIC_DISABLE_PYDANTIC_V2_PLUGINS'] = '1'
   ```

2. **修补 inspect 模块**：
   ```python
   def _patched_getsource(object):
       try:
           return _original_getsource(object)
       except (OSError, TypeError):
           return "# Source code not available"
   ```

这样即使 `logfire` 或其他库调用 `inspect.getsource()`，也不会崩溃。

## 🚀 重新打包

### 步骤 1：清理旧文件

```bash
rm -rf build dist
```

### 步骤 2：重新打包

```bash
# 确保在虚拟环境中
python build.py
# 选择选项 1 (GUI 版本)
```

### 步骤 3：解除隔离属性

```bash
xattr -cr dist/GarminWeightSync
xattr -cr dist/GarminWeightSync.app
```

### 步骤 4：测试

```bash
./dist/GarminWeightSync
```

## 📋 完整的自动化脚本

你也可以使用自动修复脚本：

```bash
./fix_macos_crash.sh
```

它会自动完成所有步骤。

## 🔍 验证修复

如果成功，你应该能看到：

```bash
$ ./dist/GarminWeightSync
# GUI 窗口成功打开，没有 OSError 错误
```

## 💡 如果还有问题

### 问题 1：仍然有 inspect 错误

**解决方案**：
```bash
# 检查 pyi_rth_pyqt6.py 是否在项目根目录
ls pyi_rth_pyqt6.py

# 查看打包日志，确认 runtime hook 被包含
grep -i "runtime" build/GarminWeightSync/warn-GarminWeightSync.txt
```

### 问题 2：其他 pydantic 相关错误

**可能的解决方案**：
```bash
# 降级 pydantic 到不依赖 logfire 的版本
pip install 'pydantic<2.6'

# 或者手动卸载 logfire
pip uninstall logfire -y
```

### 问题 3：想看到更详细的错误信息

**解决方案**：
```bash
# 去掉 --windowed 参数，可以看到控制台输出
# 编辑 build.py，临时注释掉这一行：
# '--windowed',

# 重新打包
python build.py
```

## 📦 已修复的打包配置

更新后的 [build.py](build.py) 包含：

- ✅ Runtime hook：`--runtime-hook=pyi_rth_pyqt6.py`
- ✅ 所有 jaraco 模块
- ✅ logfire 完整收集
- ✅ 完整的隐藏导入列表

## 🎉 成功标志

打包成功后：

```bash
============================================================
✅ GUI 版本打包完成！
输出文件: dist/GarminWeightSync
============================================================

$ ./dist/GarminWeightSync
# 窗口正常打开，可以正常使用！
```

## 📞 如果问题依然存在

请提供：

1. **完整的错误日志**：
   ```bash
   ./dist/GarminWeightSync 2>&1 | tee error_log.txt
   ```

2. **PyInstaller 警告文件**：
   ```bash
   cat build/GarminWeightSync/warn-GarminWeightSync.txt
   ```

3. **环境信息**：
   ```bash
   pip list | grep -i "pydantic\|logfire"
   ```

---

**版本**: 2.0
**最后更新**: 2026-01-14
**状态**: ✅ 已添加 runtime hook 修复 inspect 错误
