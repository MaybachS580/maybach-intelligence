"""
报告生成器
输出：Markdown报告 + HTML看板 + JSON数据
"""

import os
import json
from datetime import datetime
from pathlib import Path

TEMPLATE_MARKDOWN = """# 📊 迈巴赫商业情报台 - 分析报告

> 生成时间: {run_at}
> 监测关键词: {keywords}

---

## 🔥 一、热门话题概览

{topics_summary}

---

## 🧠 二、AI趋势洞察

{insights_text}

---

## 💡 三、内容选题方案（Top 10）

{ideas_text}

---

## 💰 四、变现机会矩阵

{opportunities_text}

---

## 🎯 五、行动建议

{action_text}

---

*报告由迈巴赫商业情报台自动生成 | MaybachS580/maybach-intelligence*
"""


class ReportGenerator:
    """多格式报告生成"""

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate(self, results: dict) -> str:
        """
        生成完整报告
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        keyword_str = "+".join(results["keywords"])
        base_name = f"report_{keyword_str}_{timestamp}"

        # Markdown报告
        md_path = self.output_dir / f"{base_name}.md"
        md_path.write_text(self._build_markdown(results), encoding="utf-8")

        # JSON原始数据
        json_path = self.output_dir / f"{base_name}.json"
        json_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

        return str(md_path)

    def _build_markdown(self, results: dict) -> str:
        topics = results.get("topics", {})
        keywords = results.get("keywords", [])

        # 话题摘要
        topics_lines = []
        for kw, items in topics.items():
            if items:
                top = items[0].get("title", "N/A")
                count = len(items)
                topics_lines.append(f"- **{kw}**：{count}条话题，最热：「{top}」")
        topics_summary = "\n".join(topics_lines) if topics_lines else "暂无数据"

        # 洞察
        insights_lines = []
        for ins in results.get("insights", []):
            kw = ins.get("keyword", "")
            direction = ins.get("direction", ins.get("raw_analysis", ""))
            gap = ins.get("gap", "")
            insights_lines.append(f"### {kw}\n**方向**：{direction}\n**空白点**：{gap}")
        insights_text = "\n\n".join(insights_lines) if insights_lines else "暂无洞察"

        # 选题
        ideas = results.get("content_ideas", [])
        ideas_text = ""
        for i, idea in enumerate(ideas[:10], 1):
            title = idea.get("title", "N/A")
            script = idea.get("script", idea.get("raw", ""))
            ideas_text += f"{i}. **{title}**\n   {script}\n\n"

        # 变现
        opps = results.get("opportunities", [])
        opps_text = ""
        for opp in opps:
            title = opp.get("title", "N/A")
            model = opp.get("model", "N/A")
            revenue = opp.get("est_revenue", "N/A")
            diff = opp.get("difficulty", "N/A")
            opps_text += f"- **{title}** | 模式: {model} | 收益: {revenue} | 难度: {diff}\n"

        # 行动建议
        top_opp = opps[0] if opps else {}
        action_text = f"""基于本次分析，推荐优先启动：
1. **选题方向**：{ideas[0].get('title', '待定')}（预计{ideas[0].get('expected', 'N/A')}）
2. **变现模式**：{top_opp.get('model', '待定')}（预估{top_opp.get('est_revenue', 'N/A')}）
3. **启动路径**：{top_opp.get('path', '待定')}"""

        return TEMPLATE_MARKDOWN.format(
            run_at=results.get("run_at", ""),
            keywords=" | ".join(keywords),
            topics_summary=topics_summary,
            insights_text=insights_text,
            ideas_text=ideas_text or "暂无选题",
            opportunities_text=opps_text or "暂无变现机会",
            action_text=action_text,
        )
