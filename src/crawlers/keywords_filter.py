"""关键词筛选模块"""
from typing import List, Dict, Optional
from functools import lru_cache

from ..models import Article
from ..config.reader import ConfigReader


# 全局缓存关键词（小写版本，用于快速匹配）
_KEYWORDS_CACHE = {"legend": {}, "front": set(), "initialized": False}

# 原始关键词（保留大小写，用于 _load_keywords 兼容）
_ORIGINAL_KEYWORDS = {"legend": {}, "front": []}


def _init_keywords():
    """初始化关键词缓存（只执行一次）"""
    if _KEYWORDS_CACHE["initialized"]:
        return

    try:
        reader = ConfigReader()
        config = reader.load_news_keywords_config()

        # 解析 legend 关键词
        legend_config = config.get("legend", {})
        for legend_id, keyword_groups in legend_config.items():
            keywords_lower = set()  # 小写版本用于匹配
            keywords_original = []  # 原始版本保留
            if isinstance(keyword_groups, list):
                for group in keyword_groups:
                    if isinstance(group, list):
                        for kw in group:
                            if kw and kw.strip():
                                keywords_lower.add(kw.lower())
                                keywords_original.append(kw)
                    elif isinstance(group, str):
                        if group and group.strip():
                            keywords_lower.add(group.lower())
                            keywords_original.append(group)
            _KEYWORDS_CACHE["legend"][legend_id] = keywords_lower
            _ORIGINAL_KEYWORDS["legend"][legend_id] = keywords_original

        # 解析 front 关键词
        front_config = config.get("front", [])
        front_lower = set()  # 小写版本
        front_original = []  # 原始版本
        for group in front_config:
            if isinstance(group, list):
                for kw in group:
                    if kw and kw.strip():
                        front_lower.add(kw.lower())
                        front_original.append(kw)
            elif isinstance(group, str):
                if group and group.strip():
                    front_lower.add(group.lower())
                    front_original.append(group)
        _KEYWORDS_CACHE["front"] = front_lower
        _ORIGINAL_KEYWORDS["front"] = front_original

        _KEYWORDS_CACHE["initialized"] = True

        # 打印调试信息
        total_legend_kw = sum(len(kws) for kws in _KEYWORDS_CACHE["legend"].values())
        print(f"[Debug] Legend 关键词数: {total_legend_kw}")
        print(f"[Debug] Front 关键词数: {len(_KEYWORDS_CACHE['front'])}")
    except Exception as e:
        print(f"Warning: Failed to load keywords config: {e}")
        import traceback
        traceback.print_exc()


def _match_legend(text: str) -> Optional[str]:
    """匹配 legend 关键词（使用生成器 + any，短路优化）

    Args:
        text: 要匹配的文本（已小写）

    Returns:
        命中的 legend_id，未命中返回 None
    """
    for legend_id, keywords in _KEYWORDS_CACHE["legend"].items():
        if any(kw in text for kw in keywords):
            return legend_id
    return None


def _match_front(text: str) -> bool:
    """匹配 front 关键词（使用 any，短路优化）

    Args:
        text: 要匹配的文本（已小写）

    Returns:
        是否命中
    """
    return any(kw in text for kw in _KEYWORDS_CACHE["front"])


def filter_by_keywords(articles: List[Article]) -> List[Article]:
    """根据关键词过滤文章并标注 legend

    匹配逻辑:
    1. 先匹配 legend 关键词组 → 命中则设置 article.legend = 对应的 legend_id
    2. 再匹配 front 关键词组 → 命中则 article.legend = None
    3. 都未命中 → 丢弃文章

    Args:
        articles: 待过滤的文章列表

    Returns:
        匹配关键词的文章列表，legend 字段已标注
    """
    # 确保关键词已初始化
    _init_keywords()

    legend_keywords = _KEYWORDS_CACHE["legend"]
    front_keywords = _KEYWORDS_CACHE["front"]

    # 统计信息
    legend_counts = {legend_id: 0 for legend_id in legend_keywords.keys()}
    front_count = 0
    unmatched_count = 0

    filtered = []
    for article in articles:
        # 只匹配标题，不匹配 URL（URL 可能包含随机字符串导致误匹配）
        text_to_check = article.title.lower()

        # 1. 先匹配 legend 关键词
        matched_legend_id = _match_legend(text_to_check)

        if matched_legend_id:
            article.legend = matched_legend_id
            legend_counts[matched_legend_id] += 1
            filtered.append(article)
            continue

        # 2. 再匹配 front 关键词
        if _match_front(text_to_check):
            article.legend = None
            front_count += 1
            filtered.append(article)
        else:
            unmatched_count += 1
            if unmatched_count <= 5:  # 打印前5个没匹配的
                print(f"[Filter] 未匹配: {article.title[:50]}...")

    # 打印统计信息
    total_legend = sum(legend_counts.values())
    print(f"[Filter] Legend 匹配: {total_legend} (详情: {legend_counts})")
    print(f"[Filter] Front 匹配: {front_count}")
    print(f"[Filter] 未匹配: {unmatched_count}")
    print(f"[Filter] 总计: {len(filtered)}/{len(articles)}")

    return filtered


def _load_keywords() -> Dict:
    """从配置文件加载关键词（保留用于兼容旧代码）

    返回:
        {
            'legend': {
                'musk': ['关键词1', '关键词2', ...],
                'huang': ['关键词1', '关键词2', ...],
            },
            'front': ['关键词1', '关键词2', ...]
        }
    """
    _init_keywords()
    return _ORIGINAL_KEYWORDS
