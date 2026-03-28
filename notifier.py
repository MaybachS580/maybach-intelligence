"""
微信推送通知器
使用 wxauto 往指定联系人发送分析报告摘要
"""

import os
import sys
import time
from datetime import datetime
from typing import Optional

# wxauto 路径
WX_PYTHON = r"C:\Users\lenovo\.workbuddy\binaries\python\versions\3.13.12\python.exe"
WX_PATH = r"C:\Program Files\Tencent\Weixin\Weixin.exe"


class WeChatNotifier:
    """微信消息推送器"""

    def __init__(self, contact_name: str = "文件传输助手"):
        self.contact_name = contact_name
        self.wx = None

    def connect(self, max_retries: int = 3) -> bool:
        """
        连接微信客户端
        """
        try:
            sys.path.insert(0, r"C:\Users\lenovo\.workbuddy\binaries\python\versions\3.13.12\Lib\site-packages")
            import wxauto

            print(f"    [微信] 正在连接微信客户端...")
            self.wx = wxauto.WxAuto()
            self.wx.CheckLogin()

            print(f"    [微信] ✅ 已连接微信")
            return True

        except Exception as e:
            print(f"    [微信] ❌ 连接失败: {e}")
            return False

    def send_text(self, message: str) -> bool:
        """
        发送文本消息
        """
        if not self.wx:
            print("    [微信] ⚠️ 未连接微信")
            return False

        try:
            self.wx.SendMsg(message, self.contact_name)
            print(f"    [微信] ✅ 消息已发送至「{self.contact_name}」")
            return True
        except Exception as e:
            print(f"    [微信] ❌ 发送失败: {e}")
            return False

    def send_report_summary(self, results: dict) -> bool:
        """
        发送报告摘要卡片
        """
        keywords = results.get("keywords", [])
        opportunities = results.get("opportunities", [])
        insights = results.get("insights", [])
        ideas = results.get("content_ideas", [])
        run_at = results.get("run_at", "")[:16].replace("T", " ")

        lines = [
            f"🏎️ 迈巴赫商业情报报告",
            f"📅 {run_at}",
            "=" * 30,
            "",
            f"📊 监测领域: {' | '.join(keywords)}",
            "",
            f"🔍 发现 {len(insights)} 条洞察",
            f"💡 产出 {len(ideas)} 个选题",
            f"💰 识别 {len(opportunities)} 个变现机会",
            "",
            "─" * 30,
            "TOP 3 变现机会：",
        ]

        for i, opp in enumerate(opportunities[:3], 1):
            title = opp.get("title", "N/A")
            model = opp.get("model", "")
            revenue = opp.get("est_revenue", "")
            diff = opp.get("difficulty", "")
            lines.append(f"{i}. {title}")
            if model:
                lines.append(f"   模式: {model} | 收益: {revenue} | 难度: {diff}")

        lines.extend(["", "─" * 30, "详细报告: D:\\maybach-intelligence\\reports"])

        message = "\n".join(lines)
        return self.send_text(message)

    def send_heartbeat(self, message: str = "✅ 迈巴赫心跳还在跳 🏎️💰") -> bool:
        """
        发送心跳信号
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        return self.send_text(f"{message}\n⏰ {timestamp}")


# ─── 便捷函数 ─────────────────────────────────────────────

def quick_notify(results: dict, contact: str = "文件传输助手") -> bool:
    """
    一行代码发送报告摘要
    """
    notifier = WeChatNotifier(contact_name=contact)
    if not notifier.connect():
        return False
    return notifier.send_report_summary(results)


def quick_heartbeat(message: str = None, contact: str = "文件传输助手") -> bool:
    """
    一行代码发送心跳
    """
    notifier = WeChatNotifier(contact_name=contact)
    if not notifier.connect():
        return False
    return notifier.send_heartbeat(message or f"✅ 迈巴赫心跳 | {datetime.now().strftime('%Y-%m-%d %H:%M')}")


if __name__ == "__main__":
    # 测试心跳
    print("测试微信连接...")
    result = quick_heartbeat("🏎️ 迈巴赫上线测试")
    if result:
        print("✅ 测试消息已发送")
    else:
        print("❌ 请确保微信已登录运行")
