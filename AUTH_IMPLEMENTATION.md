# 小米账号密码登录功能实现说明

## 功能概述

已实现当用户没有小米 Token 时,通过用户名密码自动登录的功能,支持:
- ✅ 验证码输入
- ✅ 二次验证码(2FA/MFA)输入
- ✅ 登录成功后自动保存 Token 到配置文件
- ✅ 友好的 GUI 对话框交互

## 使用方法

### 1. 准备配置文件

复制 `users.example.json` 为 `users.json`:

```bash
cp users.example.json users.json
```

### 2. 编辑配置文件

在 `users.json` 中填入您的账号信息:

```json
{
  "users": [
    {
      "username": "your_xiaomi_username",  // 小米账号用户名或手机号
      "password": "your_xiaomi_password",   // 小米账号密码
      "model": "yunmai.scales.ms103",       // 体重秤型号
      "token": null,                        // 首次使用留空
      "garmin": {
        "email": "your_garmin_email@example.com",  // Garmin 邮箱
        "password": "your_garmin_password",        // Garmin 密码
        "domain": "CN",                      // CN 或 COM
        "filter": null
      },
      "last_sync": null,
      "created_at": null
    }
  ]
}
```

**重要提示**:
- 首次使用时,`token` 字段设置为 `null`
- 确保小米账号的用户名和密码正确
- Garmin 信息也需要正确填写

### 3. 启动应用并同步

```bash
python src/gui/main.py users.json
```

或者在项目根目录:

```bash
python -m src.gui.main users.json
```

### 4. 登录流程

1. 点击"同步"按钮
2. 如果没有 Token,会自动触发登录流程
3. **情况1 - 直接登录成功**: 如果账号不需要验证码,直接登录成功并继续同步
4. **情况2 - 需要验证码**: 弹出验证码对话框,输入图片中的验证码
5. **情况3 - 需要 2FA**: 弹出二次验证对话框,输入手机或邮箱收到的验证码
6. 登录成功后,Token 会自动保存到 `users.json` 中
7. 下次同步时将直接使用 Token,无需再次登录

## 新增文件

### 1. `src/gui/auth_dialogs.py`

包含两个对话框类:

**CaptchaDialog** - 验证码输入对话框
- 显示验证码图片
- 验证码输入框
- 确定/取消按钮

**MfaDialog** - 二次验证码输入对话框
- 显示验证说明
- 验证码输入框
- 确定/取消按钮

### 2. `test_auth_dialogs.py`

对话框测试脚本,可用于验证对话框功能:

```bash
python test_auth_dialogs.py
```

## 修改的文件

### 1. `src/gui/main_window.py`

**修改内容**:
- `SyncWorker` 类添加队列机制,支持双向通信
- `on_sync_progress` 方法添加 `awaiting_input` 阶段处理
- 新增登录处理方法:
  - `handle_user_input_request()` - 处理用户输入请求
  - `_handle_xiaomi_login_async()` - 异步处理小米登录
  - `_show_captcha_dialog()` - 显示验证码对话框
  - `_show_mfa_dialog()` - 显示 2FA 对话框
  - `_extract_token_data()` - 提取 Token 数据
  - `_send_login_result()` - 发送登录结果回同步线程

### 2. `src/core/sync_service.py`

**修改内容**:
- `sync_user()` 方法添加 `input_callback` 参数
- 在无 Token 时调用 `input_callback` 请求用户登录
- 登录成功后自动保存 Token 并继续同步

## 技术细节

### 数据流

```
用户点击同步
    ↓
SyncWorker.run()
    ↓
SyncOrchestrator.sync_user(username, input_callback)
    ↓
检测无 Token
    ↓
调用 input_callback({"action": "xiaomi_login", ...})
    ↓
SyncWorker.get_user_input() 阻塞等待
    ↓
发送 "awaiting_input" 信号到 GUI
    ↓
MainWindow.handle_user_input_request()
    ↓
_handle_xiaomi_login_async() (后台线程)
    ↓
MiCloudSync.login()
    ↓
┌─────────────┬──────────────┬──────────────┐
│ 直接成功     │ 需要验证码    │ 需要 2FA     │
└─────────────┴──────────────┴──────────────┘
     ↓              ↓              ↓
 返回 Token    弹出对话框      弹出对话框
     ↓              ↓              ↓
   继续        提交验证码      提交验证码
                      ↓              ↓
                   返回 Token    返回 Token
                          ↓            ↓
                        _send_login_result()
                          ↓
                    SyncWorker.provide_input()
                          ↓
                    get_user_input() 返回
                          ↓
                    继续同步流程
```

### 线程安全

- 登录操作在独立的后台线程中执行,避免阻塞 GUI
- 使用 `queue.Queue` 实现线程间通信
- 使用 `QTimer.singleShot(0, ...)` 确保对话框在主线程显示

### 错误处理

1. **用户取消**: 返回 `{"success": False, "error": "用户取消"}`
2. **验证码错误**: 自动重新显示验证码对话框
3. **2FA 错误**: 显示错误提示,允许重新输入
4. **网络错误**: 捕获异常并返回错误信息
5. **Token 提取失败**: 记录日志并返回默认空 Token

## 测试建议

### 测试场景 1: 无验证码直接登录

1. 准备一个不需要验证码的小米账号
2. 配置 `users.json`,不填写 token
3. 启动应用并同步
4. 预期: 直接登录成功并继续同步

### 测试场景 2: 需要验证码

1. 准备一个需要验证码的小米账号
2. 配置 `users.json`
3. 启动应用并同步
4. 预期: 弹出验证码对话框,输入正确验证码后继续

### 测试场景 3: 需要 2FA

1. 准备一个开启了 2FA 的小米账号
2. 配置 `users.json`
3. 启动应用并同步
4. 预期: 弹出 2FA 对话框,输入正确验证码后继续

### 测试场景 4: 验证码错误

1. 触发验证码对话框
2. 输入错误的验证码
3. 预期: 重新显示验证码对话框

### 测试场景 5: 用户取消

1. 触发验证码或 2FA 对话框
2. 点击取消按钮
3. 预期: 同步终止,显示取消提示

### 测试场景 6: 已有 Token

1. 首次登录成功后,Token 已保存
2. 再次同步
3. 预期: 直接使用 Token,不弹出登录对话框

## 注意事项

1. **密码安全**:
   - 当前密码以明文存储在 `users.json` 中
   - 建议设置合适的文件权限(如 `chmod 600 users.json`)
   - 后续可考虑加密存储

2. **Token 有效期**:
   - 小米 Token 通常长期有效
   - 如果 Token 过期,会自动重新登录
   - 建议定期备份 `users.json`

3. **并发限制**:
   - 当前实现不支持多用户并发登录
   - 多用户同步时,会依次处理每个用户

4. **网络要求**:
   - 登录过程需要网络连接
   - 验证码图片需要从小米服务器下载
   - 建议在网络稳定的环境下使用

## 故障排除

### 问题1: 登录失败,提示"缺少用户名或密码"

**解决方案**: 检查 `users.json` 中是否正确填写了 `username` 和 `password` 字段

### 问题2: 验证码对话框显示空白

**解决方案**: 检查网络连接,确保可以访问小米服务器

### 问题3: 2FA 验证码输入错误

**解决方案**:
- 确保输入的是手机或邮箱收到的完整验证码
- 检查验证码是否过期(通常 5-10 分钟有效期)
- 尝试重新获取新的验证码

### 问题4: Token 保存失败

**解决方案**:
- 检查 `users.json` 文件权限
- 确保磁盘有足够空间
- 查看日志文件了解详细错误信息

## 后续优化建议

1. **密码加密**: 实现密码的加密存储
2. **异步登录**: 改为完全异步的登录流程,支持多用户并发
3. **Token 自动刷新**: 在后台自动刷新即将过期的 Token
4. **登录历史**: 记录登录历史,方便排查问题
5. **二维码登录**: 支持手机扫码登录(如果小米 API 支持)

## 反馈与支持

如果遇到问题或有建议,请通过以下方式反馈:
- 提交 GitHub Issue
- 查看项目文档
- 联系项目维护者

---

**实现日期**: 2026-01-16
**版本**: v2.0
**作者**: Claude Code
