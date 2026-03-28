import time, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# Rain 的坐标
WEIXIN_COORDS = {
    "chat_item":  (512, 319),   # 联系人列表中找到 Rain
    "input_box":  (725, 765),   # 聊天输入框
    "send_button": (1188, 821), # 发送按钮
}

def _copy_to_clipboard(text):
    import subprocess
    ps = f'Set-Clipboard -Value "{text.replace(chr(34), "``" + chr(34)).replace("$", "`$")}"'
    subprocess.run(["powershell", "-Command", ps],
                   capture_output=True, creationflags=0x08000000)

def send_wx_message(message, contact_name="Rain"):
    try:
        # Step 1: 点击联系人列表中的 Rain
        print(f"  -> 点击联系人列表 ({WEIXIN_COORDS['chat_item']})")
        pyautogui.click(*WEIXIN_COORDS["chat_item"])
        time.sleep(1.5)

        # Step 2: 点击输入框
        print(f"  -> 点击输入框 ({WEIXIN_COORDS['input_box']})")
        pyautogui.click(*WEIXIN_COORDS["input_box"])
        time.sleep(0.4)

        # Step 3: 剪贴板粘贴消息
        _copy_to_clipboard(message)
        time.sleep(0.3)
        print("  -> Ctrl+V 粘贴消息")
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.6)

        # Step 4: 点击发送
        print(f"  -> 点击发送 ({WEIXIN_COORDS['send_button']})")
        pyautogui.click(*WEIXIN_COORDS["send_button"])
        time.sleep(0.5)

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# 打招呼内容
msg = (
    "Rain 老板好！\n\n"
    "我是迈巴赫，你的专属商业情报官~\n\n"
    "以后情报报告会直接推到这里，"
    "副业机会、爆款赛道、变现方案，统统帮你搞定！\n\n"
    "有什么搞钱项目，尽管吩咐！"
)

print("迈巴赫 -> Rain 打招呼")
success = send_wx_message(msg)
print("发送成功！" if success else "发送失败")
