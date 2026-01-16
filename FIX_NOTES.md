# 修复说明

## 问题
登录时验证码对话框没有弹出

## 原因
1. **Token 数据格式不匹配**: `MiCloudSync` 返回的 token 格式是 `"userId:passToken"` 字符串,而代码期望的是字典格式
2. **线程安全问题**: 在后台线程中尝试显示对话框,导致线程安全问题

## 修复内容

### 1. 修复 Token 数据提取 ([src/gui/main_window.py:815-838](src/gui/main_window.py:815-838))

```python
def _extract_token_data(self, result: Dict[str, Any], micloud_sync) -> Dict[str, str]:
    """从登录结果中提取 token 数据"""
    import base64

    # MiCloudSync 返回的 token 格式是 "userId:passToken"
    token_string = result.get("token", "")

    if not token_string:
        return {"userId": "", "passToken": "", "ssecurity": ""}

    # 解析 token 字符串
    if ":" in token_string:
        user_id, pass_token = token_string.split(":", 1)
    else:
        user_id = token_string
        pass_token = ""

    # 从 micloud_sync 实例获取 ssecurity (已经是 bytes,需要 base64 编码)
    if micloud_sync.ssecurity:
        ssecurity = base64.b64encode(micloud_sync.ssecurity).decode('utf-8')
    else:
        ssecurity = ""

    return {
        "userId": user_id,
        "passToken": pass_token,
        "ssecurity": ssecurity
    }
```

### 2. 改为同步处理 ([src/gui/main_window.py:664-724](src/gui/main_window.py:664-724))

将登录处理改为在主线程中同步执行,避免线程安全问题:

```python
def handle_user_input_request(self, progress: SyncProgress):
    """处理用户输入请求"""
    details = progress.details
    action = details.get("action")

    if action == "xiaomi_login":
        # 直接在主线程中处理登录(同步方式)
        result = self._handle_xiaomi_login(progress.username, details)
        # 将结果发送回工作线程
        self._send_login_result(progress.username, result)
```

### 3. 对话框返回结果 ([src/gui/main_window.py:726-813](src/gui/main_window.py:726-813))

对话框方法现在直接返回结果字典,而不是通过回调:

```python
def _show_captcha_dialog_sync(self, username: str, captcha_image: bytes, micloud_sync, retry_count: int = 0) -> Dict[str, Any]:
    """显示验证码对话框(同步版本,返回结果)"""
    # ... 显示对话框
    if dialog.exec() == 1:
        # 处理验证码
        if result.get("ok"):
            return {"success": True, "token": token_data}
        # ...

    return {"success": False, "error": "用户取消"}
```

### 4. 添加重试机制

验证码和 2FA 输入错误时,自动重新显示对话框,最多重试 3 次。

## 测试步骤

1. 准备一个需要验证码的小米账号
2. 在 `users.json` 中配置账号信息,确保 `token` 为 `null`
3. 启动应用并点击同步
4. 应该会弹出验证码对话框
5. 输入验证码后继续登录流程

## 注意事项

- 验证码对话框会自动显示,无需手动操作
- 输入错误会提示重新输入(最多 3 次)
- 登录成功后 Token 会自动保存到 `users.json`
- 下次同步将直接使用 Token,无需重新登录
