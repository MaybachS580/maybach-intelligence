"""
迈巴赫商业情报台 - 微信通知模块 (剪贴板 + pyautogui 方案)
修复 emoji 无法输入的问题
"""

import time
import os
import sys
import io

# 强制 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pyautogui

# 安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# ─── 微信 UI 坐标（Rain 默认）─────────────────────────────
WEIXIN_COORDS = {
    "chat_item":   (512, 319),   # 联系人列表项
    "input_box":   (725, 765),   # 聊天输入框
    "send_button": (1188, 821),  # 发送按钮
}


def _copy_to_clipboard(text: str) -> None:
    """把文字复制到剪贴板（Windows 专用）"""
    import subprocess
    # 用 PowerShell 设置剪贴板内容
    ps_script = f'''
    Set-Clipboard -Value "{text.replace('"', '`"').replace('$', '`$')}"
    '''
    subprocess.run(
        ["powershell", "-Command", ps_script],
        capture_output=True, creationflags=0x08000000  # CREATE_NO_WINDOW
    )


def send_wx_message(message: str, contact: str = "文件传输助手") -> bool:
    """
    发送微信消息（支持 emoji + 中文）
    流程：搜索联系人 → 进入聊天 → 剪贴板粘贴 → 发送
    """
    try:
        # Step 1: 点击联系人列表中的联系人
        pyautogui.click(*WEIXIN_COORDS["chat_item"])
        time.sleep(1.5)

        # Step 2: 点击输入框
        pyautogui.click(*WEIXIN_COORDS["input_box"])
        time.sleep(0.4)

        # Step 5: 复制消息到剪贴板，然后 Ctrl+V 粘贴（支持 emoji）
        _copy_to_clipboard(message)
        time.sleep(0.3)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.6)

        # Step 6: 点击发送按钮
        pyautogui.click(*WEIXIN_COORDS["send_button"])
        time.sleep(0.5)

        return True

    except Exception as e:
        print(f"[send_wx_message] Error: {e}")
        return False


def format_report_message(results: dict) -> str:
    """将分析结果格式化为微信消息（纯文本，emoji可用）"""
    run_at   = results.get("run_at", "")[:16]
    keywords = ", ".join(results.get("keywords", []))

    opportunities = results.get("opportunities", [])[:3]
    op_lines = []
    for i, op in enumerate(opportunities, 1):
        title = op.get("title", "N/A")
        revenue = op.get("est_revenue", "N/A")
        difficulty = op.get("difficulty", "N/A")
        op_lines.append(f"{i}. {title}")
        op_lines.append(f"   收益: {revenue} | 难度: {difficulty}")

    ideas = results.get("content_ideas", [])[:2]
    idea_lines = []
    for i, idea in enumerate(ideas, 1):
        title = idea.get("title", "N/A")
        platform = idea.get("platform", "N/A")
        idea_lines.append(f"{i}. {title} | {platform}")

    msg = "迈巴赫情报台 | " + run_at + "\n" + \
          "============================\n" + \
          "监测关键词：" + keywords + "\n\n" + \
          "【变现机会 Top 3】\n" + \
          ("\n".join(op_lines) if op_lines else "暂无高价值机会") + "\n\n" + \
          "【优质选题 Top 2】\n" + \
          ("\n".join(idea_lines) if idea_lines else "暂无优质选题") + "\n" + \
          "============================\n" + \
          "完整报告 -> D:\\maybach-intelligence\\reports\\"

    return msg


def quick_notify(results: dict, contact: str = "文件传输助手") -> bool:
    """一行命令发送报告摘要到微信"""
    msg = format_report_message(results)
    return send_wx_message(msg, contact=contact)


def send_test_greeting(contact: str = "文件传输助手") -> bool:
    """发送打招呼消息"""
    msg = (
        "老板晚上好！\n\n"
        "我是迈巴赫，你的商业情报官~\n\n"
        "以后情报报告会直接推到这里，随时汇报！\n\n"
        "有什么需要搞钱的项目，尽管吩咐！"
    )
    return send_wx_message(msg, contact=contact)


if __name__ == "__main__":
    print("迈巴赫微信通知 - 测试打招呼")
    success = send_test_greeting()
    if success:
        print("发送成功！")
    else:
        print("发送失败，请检查微信是否在前台")
