"""关键词筛选模块"""
from typing import List

from ..models import Article
from ..config.reader import ConfigReader


def filter_by_keywords(articles: List[Article]) -> List[Article]:
    """根据关键词过滤文章

    Args:
        articles: 待过滤的文章列表

    Returns:
        匹配关键词的文章列表
    """
    # 加载关键词
    all_keywords = _load_keywords()

    if not all_keywords:
        print("[Filter] 关键词为空，返回所有文章")
        return articles

    print(f"[Filter] 加载关键词数: {len(all_keywords)}")
    print(f"[Filter] 前10个关键词: {all_keywords[:10]}")

    filtered = []
    unmatched_count = 0
    for article in articles:
        # 只匹配标题，不匹配 URL（URL 可能包含随机字符串导致误匹配）
        text_to_check = article.title.lower()
        matched = False
        for kw in all_keywords:
            if kw.lower() in text_to_check:
                matched = True
                break

        if matched:
            filtered.append(article)
        else:
            unmatched_count += 1
            if unmatched_count <= 5:  # 打印前5个没匹配的
                print(f"[Filter] 未匹配: {article.title[:50]}...")

    print(f"[Filter] 关键词数量: {len(all_keywords)}, 过滤后: {len(filtered)}/{len(articles)}")
    return filtered


def _load_keywords() -> List[str]:
    """从配置文件加载关键词"""
    try:
        reader = ConfigReader()
        config = reader.load_news_keywords_config()

        # 展平所有关键词
        all_keywords = set()

        # 人物关键词
        for person_keywords in config.get("people", {}).values():
            all_keywords.update(person_keywords)

        # 公司关键词
        for company_keywords in config.get("companies", {}).values():
            all_keywords.update(company_keywords)

        # 话题关键词
        for topic_group in config.get("topics", []):
            all_keywords.update(topic_group)

        # 过滤掉空字符串和纯空格
        all_keywords = {kw for kw in all_keywords if kw and kw.strip()}

        print(f"[Debug] 加载关键词前: {len(all_keywords)}")
        # 检查是否有空格
        if ' ' in all_keywords or '' in all_keywords:
            print(f"[Debug] 发现空格或空字符串!")
            all_keywords.discard(' ')
            all_keywords.discard('')

        return list(all_keywords)
    except Exception as e:
        print(f"Warning: Failed to load keywords config: {e}")
        import traceback
        traceback.print_exc()
        return []
