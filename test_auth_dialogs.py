#!/usr/bin/env python3
"""
测试认证对话框
用于验证验证码和 2FA 对话框的基本功能
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from PyQt6.QtWidgets import QApplication
from gui.auth_dialogs import CaptchaDialog, MfaDialog


def test_captcha_dialog():
    """测试验证码对话框"""
    print("测试验证码对话框...")

    # 创建一个模拟的验证码图片(纯色图片)
    from PyQt6.QtGui import QImage, QPixmap
    import io

    # 创建一个简单的测试图片
    image = QImage(400, 80, QImage.Format.Format_RGB32)
    image.fill(0xFFFFFF)  # 白色背景

    # 保存为字节
    buffer = QtCore.QByteArray()
    buffer2 = QtCore.QBuffer(buffer)
    buffer2.open(QtCore.QBuffer.OpenModeFlag.WriteOnly)
    image.save(buffer2, "PNG")
    captcha_bytes = bytes(buffer.data())

    app = QApplication(sys.argv)

    dialog = CaptchaDialog(captcha_bytes)
    result = dialog.exec()

    if result == 1:
        code = dialog.get_code()
        print(f"✅ 验证码对话框测试成功,输入的验证码: {code}")
    else:
        print("❌ 验证码对话框被取消")


def test_mfa_dialog():
    """测试 2FA 对话框"""
    print("\n测试 2FA 对话框...")

    app = QApplication(sys.argv)

    dialog = MfaDialog("验证码已发送到您的手机,请查收")
    result = dialog.exec()

    if result == 1:
        code = dialog.get_ticket()
        print(f"✅ 2FA 对话框测试成功,输入的验证码: {code}")
    else:
        print("❌ 2FA 对话框被取消")


if __name__ == "__main__":
    from PyQt6 import QtCore

    print("=" * 50)
    print("认证对话框测试")
    print("=" * 50)

    # 测试验证码对话框
    test_captcha_dialog()

    # 测试 2FA 对话框
    test_mfa_dialog()

    print("\n" + "=" * 50)
    print("测试完成!")
    print("=" * 50)
