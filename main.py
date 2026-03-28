"""
迈巴赫商业情报台 - 主入口
AI驱动的社交媒体情报分析 & 内容选题生成器
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Optional

# 核心模块
from scraper import SocialMediaScraper
from analyzer import ContentAnalyzer
from reporter import ReportGenerator

# 通知模块（可选）
try:
    from notifier import WeChatNotifier, quick_notify
    NOTIFIER_AVAILABLE = True
except ImportError:
    NOTIFIER_AVAILABLE = False
    print("⚠️  未安装 wxauto，微信推送功能不可用")

# 默认API配置（支持 OpenAI / Claude / 通义千问 等）
DEFAULT_CONFIG = {
    "api_provider": "openai",   # openai | claude | dashscope
    "model": "gpt-4o-mini",
    "api_key": os.getenv("OPENAI_API_KEY", ""),
}

class MaybachIntelligence:
    """迈巴赫商业情报台核心类"""

    def __init__(self, config: Optional[dict] = None):
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.scraper = SocialMediaScraper()
        self.analyzer = ContentAnalyzer(self.config)
        self.report = ReportGenerator()

    def run_full_pipeline(self, keywords: list[str], notify: bool = False, contact: str = "文件传输助手") -> dict:
        """
        完整pipeline：抓取 → 分析 → 生成报告 → 推送微信
        """
        print(f"\n{'='*50}")
        print(f"  迈巴赫商业情报台 | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*50}\n")

        results = {
            "run_at": datetime.now().isoformat(),
            "keywords": keywords,
            "topics": {},
            "insights": [],
            "content_ideas": [],
            "opportunities": [],
        }

        # Step 1: 抓取各平台热门话题
        print("[1/4] 抓取社交媒体热门话题...")
        for keyword in keywords:
            topics = self.scraper.fetch_trending(keyword)
            results["topics"][keyword] = topics
            print(f"    ✓ {keyword}: {len(topics)} 条话题")

        # Step 2: AI分析内容趋势
        print("\n[2/4] AI分析内容趋势与变现机会...")
        insights = self.analyzer.analyze_trends(results["topics"])
        results["insights"] = insights
        print(f"    ✓ 生成 {len(insights)} 条洞察")

        # Step 3: 生成内容选题
        print("\n[3/4] 生成内容选题方案...")
        ideas = self.analyzer.generate_content_ideas(keywords, insights)
        results["content_ideas"] = ideas
        print(f"    ✓ 生成 {len(ideas)} 个选题方案")

        # Step 4: 识别变现机会
        print("\n[4/4] 识别变现机会...")
        opportunities = self.analyzer.spot_monetization(results["insights"])
        results["opportunities"] = opportunities
        print(f"    ✓ 发现 {len(opportunities)} 个变现机会")

        # Step 5: 生成报告
        print("\n[5/5] 生成分析报告...")
        report_path = self.report.generate(results)
        print(f"    ✓ 报告已生成: {report_path}")

        # Step 6: 微信推送（可选）
        if notify and NOTIFIER_AVAILABLE:
            print(f"\n[6/6] 推送微信通知...")
            success = quick_notify(results, contact=contact)
            if success:
                print(f"    ✓ 已发送至「{contact}」")
            else:
                print(f"    ⚠️ 微信推送失败，请检查微信是否运行")

        return results


def main():
    # 默认分析的关键词（可自行修改）
    keywords = [
        "副业",
        "搞钱",
        "大学生",
        "AI工具",
        "小红书运营",
    ]

    notify = False
    contact = "文件传输助手"

    # 解析参数
    args = sys.argv[1:]
    if "--notify" in args or "-n" in args:
        notify = True
        args = [a for a in args if a not in ("--notify", "-n")]
    if "--contact" in args:
        idx = args.index("--contact")
        contact = args[idx + 1] if idx + 1 < len(args) else contact
        args = [a for a in args if a != "--contact" and a != contact]
    if args:
        keywords = args

    # 检查API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  未设置 OPENAI_API_KEY，AI分析功能不可用")
        print("   设置方式: set OPENAI_API_KEY=你的key")
        print("   将改用规则引擎进行基础分析\n")

    try:
        bot = MaybachIntelligence()
        results = bot.run_full_pipeline(keywords, notify=notify, contact=contact)

        print("\n" + "="*50)
        print("  ✅ 分析完成！Top 3 变现机会:")
        print("="*50)
        for i, opp in enumerate(results["opportunities"][:3], 1):
            print(f"  {i}. {opp.get('title', 'N/A')}")
            print(f"     预估收益: {opp.get('est_revenue', 'N/A')}")
            print(f"     难度: {opp.get('difficulty', 'N/A')}\n")

    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
