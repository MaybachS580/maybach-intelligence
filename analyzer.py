"""
AI内容分析器
基于 LLM API 分析内容趋势，生成选题和变现建议
"""

import os
import json
import time
from typing import Optional

try:
    import openai
except ImportError:
    print("请安装: pip install openai")
    raise


class ContentAnalyzer:
    """AI驱动的内容趋势分析"""

    def __init__(self, config: dict):
        self.config = config
        self.provider = config.get("api_provider", "openai")
        self._setup_client()

    def _setup_client(self):
        """根据provider初始化API客户端"""
        api_key = self.config.get("api_key") or os.getenv("OPENAI_API_KEY")

        if self.provider == "openai":
            self.client = openai.OpenAI(api_key=api_key) if api_key else None
        elif self.provider == "claude":
            # Anthropic Claude
            self.client = None
        elif self.provider == "dashscope":
            os.environ["DASHSCOPE_API_KEY"] = api_key
            self.client = None
        else:
            self.client = None

    def _call_llm(self, prompt: str, system: str = "") -> str:
        """统一LLM调用接口"""
        if not self.client:
            return self._rule_based_analysis(prompt)

        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            if self.provider == "openai":
                model = self.config.get("model", "gpt-4o-mini")
                resp = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=2000,
                )
                return resp.choices[0].message.content

        except Exception as e:
            print(f"    ⚠️ LLM调用失败: {e}")
            return self._rule_based_analysis(prompt)

    def _rule_based_analysis(self, prompt: str) -> str:
        """无API Key时的规则引擎降级"""
        return "[规则引擎模式] 请配置 OPENAI_API_KEY 以启用AI分析"

    def analyze_trends(self, topics: dict) -> list[dict]:
        """
        分析话题数据，输出洞察
        """
        insights = []
        for keyword, items in topics.items():
            if not items:
                continue

            # 构建分析prompt
            prompt = f"""你是一位顶尖的社交媒体商业分析师。请分析以下「{keyword}」领域的热门话题，找出：
            1. 最具潜力的内容方向（3个）
            2. 目标受众的痛点和需求
            3. 当前内容的空白点（没人做但有需求的方向）
            4. 爆款内容的共同特征

            热门话题数据：
            {json.dumps(items[:8], ensure_ascii=False, indent=2)}

            请用JSON格式输出，字段：insight, direction, audience_pain, gap, viral_pattern"""

            system = "你是一位专业的社交媒体商业分析师，擅长发现内容趋势和变现机会。输出简洁有力的中文分析。"
            result = self._call_llm(prompt, system)

            try:
                parsed = json.loads(result)
                insights.append({
                    "keyword": keyword,
                    "count": len(items),
                    **parsed,
                })
            except json.JSONDecodeError:
                insights.append({
                    "keyword": keyword,
                    "raw_analysis": result,
                    "count": len(items),
                })

        return insights

    def generate_content_ideas(self, keywords: list, insights: list) -> list[dict]:
        """
        根据洞察生成内容选题方案
        """
        ideas = []
        for kw in keywords:
            matching = [i for i in insights if i.get("keyword") == kw]
            direction = matching[0].get("direction", "泛生活方式内容") if matching else "泛生活方式内容"

            prompt = f"""为「{kw}」领域生成10个抖音/小红书爆款内容选题。

要求：
- 每个选题包含：标题、封面建议、正文框架、预期效果
- 标题要有钩子（悬念/数字/对比/情绪）
- 正文框架要有具体脚本思路
- 预期效果用数据区间表示

领域方向：{direction}

输出JSON数组，每个元素格式：
{{"title":"标题","cover":"封面建议","script":"正文框架","expected":"预期数据"}}"""

            system = "你是小红书/抖音爆款内容策划专家，用JSON格式输出。"
            result = self._call_llm(prompt, system)

            try:
                parsed = json.loads(result)
                for item in parsed:
                    item["keyword"] = kw
                ideas.extend(parsed)
            except json.JSONDecodeError:
                ideas.append({
                    "keyword": kw,
                    "title": f"{kw}领域爆款内容选题方案",
                    "raw": result,
                })

        return ideas

    def spot_monetization(self, insights: list) -> list[dict]:
        """
        识别变现机会
        """
        opportunities = []

        for insight in insights:
            kw = insight.get("keyword", "")
            gap = insight.get("gap", "")
            direction = insight.get("direction", "")

            prompt = f"""分析「{kw}」领域的变现机会。

已知内容方向：{direction}
内容空白点：{gap}

请从以下维度分析3个变现机会：
1. 变现模式（广告/带货/知识付费/私域/订阅等）
2. 预估月收益区间
3. 启动难度（1-5星）
4. 需要哪些资源/能力
5. 最短变现路径

输出JSON数组，每个元素：
{{"title":"机会名称","model":"变现模式","est_revenue":"预估收益","difficulty":"难度","resources":"所需资源","path":"最短路径"}}"""

            system = "你是商业变现顾问，专注于自媒体和数字经济领域。输出简洁有力的中文JSON。"
            result = self._call_llm(prompt, system)

            try:
                parsed = json.loads(result)
                opportunities.extend(parsed)
            except json.JSONDecodeError:
                pass

        return opportunities


if __name__ == "__main__":
    config = {
        "api_provider": "openai",
        "api_key": os.getenv("OPENAI_API_KEY", "sk-test"),
    }
    analyzer = ContentAnalyzer(config)
    # 测试（会走规则引擎）
    test_insights = [{"keyword": "副业", "direction": "年轻人副业指南", "gap": "缺乏实操性强的副业教程"}]
    ideas = analyzer.generate_content_ideas(["副业"], test_insights)
    print(json.dumps(ideas[:2], ensure_ascii=False, indent=2))
