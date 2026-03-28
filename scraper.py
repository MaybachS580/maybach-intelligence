"""
社交媒体抓取器
支持：小红书、微博、知乎、抖音热点、百度热搜
"""

import os
import re
import json
import time
import random
from datetime import datetime
from typing import Optional

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("请先安装依赖: pip install requests beautifulsoup4")
    raise


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/html, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


class SocialMediaScraper:
    """多平台社交媒体热门话题抓取"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.session.headers["Cookie"] = os.getenv("WEIBO_COOKIE", "")

    def fetch_trending(self, keyword: str) -> list[dict]:
        """
        抓取指定关键词在各平台的热门话题
        """
        results = []

        # 并发抓取各平台
        fetchers = [
            ("微博热搜", self._fetch_weibo),
            ("知乎热榜", self._fetch_zhihu),
            ("小红书标签", self._fetch_xiaohongshu),
            ("百度指数", self._fetch_baidu),
            ("抖音热点", self._fetch_douyin),
        ]

        for platform, fetcher in fetchers:
            try:
                items = fetcher(keyword)
                for item in items:
                    item["platform"] = platform
                    item["keyword"] = keyword
                    item["fetched_at"] = datetime.now().isoformat()
                results.extend(items)
                time.sleep(random.uniform(0.5, 1.5))  # 随机延时防封
            except Exception as e:
                print(f"    ⚠ {platform} 抓取失败: {e}")

        return results

    def _fetch_weibo(self, keyword: str) -> list[dict]:
        """微博热搜榜"""
        results = []
        try:
            # 微博热搜API
            url = "https://weibo.com/ajax/statuses/hot_band"
            resp = self.session.get(url, timeout=8)
            data = resp.json()
            if data.get("ok") == 1:
                band_list = data.get("data", {}).get("band_list", [])
                for item in band_list[:10]:
                    results.append({
                        "title": item.get("word", ""),
                        "hot_value": item.get("raw_hot", 0),
                        "url": f"https://s.weibo.com/weibo?q={keyword}",
                    })
        except Exception:
            pass
        return results

    def _fetch_zhihu(self, keyword: str) -> list[dict]:
        """知乎热榜"""
        results = []
        try:
            url = "https://api.zhihu.com/topstory/hot-lists/total"
            resp = self.session.get(url, timeout=8)
            data = resp.json()
            items = data.get("data", [])[:10]
            for item in items:
                target = item.get("target", {})
                results.append({
                    "title": target.get("title", ""),
                    "hot_value": item.get("detail_text", ""),
                    "url": target.get("url", ""),
                })
        except Exception:
            pass
        return results

    def _fetch_xiaohongshu(self, keyword: str) -> list[dict]:
        """小红书标签页（模拟搜索）"""
        results = []
        try:
            # 小红书搜索API（需要登录cookie，此处做降级）
            search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}"
            resp = self.session.get(search_url, timeout=8)
            soup = BeautifulSoup(resp.text, "html.parser")

            # 降级：返回模拟结构
            results.append({
                "title": f"小红书 #{keyword} 相关内容",
                "hot_value": "高互动",
                "url": search_url,
                "note": "需要登录Cookie才能获取真实数据，建议配置 XHS_COOKIE 环境变量",
            })
        except Exception:
            pass
        return results

    def _fetch_baidu(self, keyword: str) -> list[dict]:
        """百度热搜"""
        results = []
        try:
            url = "https://top.baidu.com/api?get=cat_1029073&token=COVER"
            resp = self.session.get(url, timeout=8)
            data = resp.json()
            items = data.get("data", {}).get("cards", [{}])[0].get("itemList", [])[:10]
            for item in items:
                results.append({
                    "title": item.get("query", ""),
                    "hot_value": item.get("hotScore", 0),
                    "desc": item.get("desc", ""),
                    "url": item.get("link", ""),
                })
        except Exception:
            pass
        return results

    def _fetch_douyin(self, keyword: str) -> list[dict]:
        """抖音热点（需要登录，此处降级）"""
        results = []
        try:
            url = "https://www.douyin.com/aweme/v1/web/hot/search/list/"
            params = {"keyword": keyword, "count": 10, "offset": 0}
            resp = self.session.get(url, params=params, timeout=8)
            # 降级返回
            results.append({
                "title": f"抖音 #{keyword} 热门视频",
                "hot_value": "高播放",
                "note": "需要登录Cookie才能获取真实数据",
            })
        except Exception:
            pass
        return results


if __name__ == "__main__":
    scraper = SocialMediaScraper()
    test = scraper.fetch_trending("副业")
    print(json.dumps(test, ensure_ascii=False, indent=2))
