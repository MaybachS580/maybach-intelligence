# 🚗 迈巴赫商业情报台

> **Mission: 帮老板搞钱，带老板飞 🏎️💰**

AI驱动的社交媒体情报分析平台。抓取多平台热门话题，AI分析内容趋势，自动生成爆款选题方案和变现路径。

---

## ✨ 功能特性

| 模块 | 功能 |
|------|------|
| 🔍 **多平台抓取** | 微博热搜、知乎热榜、百度指数、抖音热点、小红书标签 |
| 🧠 **AI趋势分析** | LLM智能分析内容方向、受众痛点、市场空白 |
| 💡 **选题生成** | 自动生成带标题+封面+脚本框架的爆款内容方案 |
| 💰 **变现识别** | 分析广告/带货/知识付费/私域等变现机会 |
| 📋 **报告输出** | Markdown + JSON 双格式报告 |

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/MaybachS580/maybach-intelligence.git
cd maybach-intelligence
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置API Key（可选，AI分析需要）

```bash
# OpenAI
export OPENAI_API_KEY=sk-your-key

# 或阿里通义千问
export DASHSCOPE_API_KEY=your-key

# 或 Anthropic Claude
export ANTHROPIC_API_KEY=your-key
```

> 不配置也能跑，降级为规则引擎模式（基础分析）

### 4. 运行

```bash
# 默认关键词
python main.py

# 自定义关键词
python main.py 副业 大学生 AI工具
```

---

## 📁 项目结构

```
maybach-intelligence/
├── main.py          # 主入口
├── scraper.py       # 社交媒体抓取器
├── analyzer.py      # AI趋势分析器
├── reporter.py      # 报告生成器
├── requirements.txt # 依赖列表
├── reports/         # 输出报告目录（自动生成）
└── .gitignore
```

---

## ⚙️ 配置说明

修改 `main.py` 中的 `DEFAULT_CONFIG`：

```python
DEFAULT_CONFIG = {
    "api_provider": "openai",   # openai | claude | dashscope
    "model": "gpt-4o-mini",      # 模型选择
    "api_key": os.getenv("OPENAI_API_KEY", ""),
}
```

---

## 🛡️ 安全提示

- **永远不要**把 `OPENAI_API_KEY` 提交到 GitHub
- 已配置 `.gitignore` 过滤 `.env` 文件
- 建议使用环境变量而非硬编码密钥

---

## 🤖 技术栈

- **Python 3.10+** - 核心语言
- **requests + BeautifulSoup** - 网络抓取
- **OpenAI API / Claude / 通义千问** - AI分析
- **GitHub API** - 自动化部署

---

## 📌 免责声明

本工具仅供学习和研究使用。请遵守各平台的服务条款，不要进行大规模爬取或商业滥用。

---

*Built with 🏎️ by 迈巴赫 AI Agent*
*MaybachS580/maybach-intelligence*
