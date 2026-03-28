"""
迈巴赫商业情报台 - 微信通知模块 (pyautogui 图像识别方案)
兼容新版 wxauto + 直接 UI 模拟双模式
"""

import time
import os
import sys
import io

# 强制 UTF-8 输出（解决 Windows GBK 问题）
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# pyautogui 配置
import pyautogui

# 安全设置：快速移动时暂停
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# ─── 微信 UI 坐标（由用户校准）───────────────────────────────
WEIXIN_COORDS = {
    "search_icon":   (386, 462),   # 搜索按钮
    "input_box":    (597, 720),   # 聊天输入框
    "send_button":  (1034, 773),  # 发送按钮
}


def send_wx_message(message: str, contact: str = "文件传输助手") -> bool:
    """
    通过 pyautogui 模拟点击发送微信消息

    Args:
        message: 要发送的消息内容
        contact: 联系人名称（默认：文件传输助手）
    """
    try:
        # Step 1: 点击搜索图标
        pyautogui.click(*WEIXIN_COORDS["search_icon"])
        time.sleep(0.8)

        # Step 2: 输入联系人名称
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.2)
        pyautogui.write(contact, interval=0.05)
        time.sleep(1.0)

        # Step 3: 按 Enter 进入聊天窗口
        pyautogui.press("enter")
        time.sleep(1.2)

        # Step 4: 点击输入框并输入消息
        pyautogui.click(*WEIXIN_COORDS["input_box"])
        time.sleep(0.3)

        # 清空输入框（Ctrl+A 全选后删除）
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.2)
        pyautogui.press("delete")
        time.sleep(0.3)

        # 写入消息
        pyautogui.write(message, interval=0.01)
        time.sleep(0.5)

        # Step 5: 点击发送按钮
        pyautogui.click(*WEIXIN_COORDS["send_button"])
        time.sleep(0.5)

        print(f"✅ 微信消息发送成功 → {contact}")
        return True

    except Exception as e:
        print(f"❌ 微信消息发送失败: {e}")
        return False


def format_report_message(results: dict) -> str:
    """
    将分析结果格式化为微信消息
    """
    run_at = results.get("run_at", "")[:16]
    keywords = ", ".join(results.get("keywords", []))

    # 取 Top 3 变现机会
    opportunities = results.get("opportunities", [])[:3]
    op_text = ""
    for i, op in enumerate(opportunities, 1):
        title = op.get("title", "N/A")
        revenue = op.get("est_revenue", "N/A")
        difficulty = op.get("difficulty", "N/A")
        op_text += f"\n{i}. 【{title}】\n   💰 {revenue} | ⭐ {difficulty}"

    if not op_text:
        op_text = "\n暂无高价值机会"

    # 取 Top 2 选题
    ideas = results.get("content_ideas", [])[:2]
    idea_text = ""
    for i, idea in enumerate(ideas, 1):
        title = idea.get("title", "N/A")
        platform = idea.get("platform", "N/A")
        idea_text += f"\n{i}. {title} | 📍{platform}"

    if not idea_text:
        idea_text = "\n暂无优质选题"

    msg = (
        f"🏎️ 迈巴赫情报台 | {run_at}\n"
        f"━━━━━━━━━━━━━━━━━\n"
        f"🔍 监测关键词：{keywords}\n"
        f"\n"
        f"💰 Top 3 变现机会：{op_text}\n"
        f"\n"
        f"💡 优质选题：{idea_text}\n"
        f"━━━━━━━━━━━━━━━━━\n"
        f"📋 完整报告 → D:\\maybach-intelligence\\reports\\"
    )
    return msg


def quick_notify(results: dict, contact: str = "文件传输助手") -> bool:
    """
    一行命令发送报告摘要到微信
    """
    msg = format_report_message(results)
    return send_wx_message(msg, contact=contact)


def send_test_message(text: str = "🏎️ 迈巴赫测试消息，收到请回复！", contact: str = "文件传输助手") -> bool:
    """
    发送测试消息（无需 results dict）
    """
    return send_wx_message(text, contact=contact)


# ─── wxauto 备选方案（如果 pyautogui 失效）────────────────
try:
    import wxauto

    def send_wxauto_message(message: str, contact: str = "文件传输助手") -> bool:
        try:
            wx = wxauto.WeChat()
            wx.SendMsg(message, contact)
            print(f"✅ wxauto 发送成功 → {contact}")
            return True
        except Exception as e:
            print(f"⚠️ wxauto 失败: {e}")
            return False

except ImportError:
    pass


if __name__ == "__main__":
    print("=" * 40)
    print("  迈巴赫微信通知模块 - 测试模式")
    print("=" * 40)
    print(f"  搜索图标: {WEIXIN_COORDS['search_icon']}")
    print(f"  输入框:   {WEIXIN_COORDS['input_box']}")
    print(f"  发送键:   {WEIXIN_COORDS['send_button']}")
    print()
    print("  确保微信在前台显示，然后我来发消息！")
    print()

    test_msg = (
        "🏎️ 迈巴赫商业情报台\n"
        "━━━━━━━━━━━━━━━━━\n"
        "✅ 微信推送通道测试成功！\n"
        "✅ 以后报告会自动推送到这里\n"
        "━━━━━━━━━━━━━━━━━\n"
        "有需要随时叫我 🚀"
    )

    success = send_wx_message(test_msg)
    if success:
        print("\n🎉 测试完成，消息已发送！")
    else:
        print("\n😢 测试失败，请检查微信是否在前台")
