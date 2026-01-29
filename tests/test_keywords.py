"""测试关键词筛选功能"""

from src.crawlers.keywords_filter import filter_by_keywords
from src.models import Article, SourceType
from datetime import datetime


def test_filter():
    """测试筛选"""

    test_articles = [
        Article(
            title="马斯克宣布星舰最新发射计划",
            url="https://example.com/spacex-starship",
            source=SourceType.IFENG,
            timestamp=datetime.now()
        ),
        Article(
            title="日经225指数低开0.2%",
            url="https://example.com/finance",
            source=SourceType.TOUTIAO,
            timestamp=datetime.now()
        ),
        Article(
            title="英伟达发布新一代AI芯片",
            url="https://example.com/nvidia",
            source=SourceType.TOUTIAO,
            timestamp=datetime.now()
        ),
        Article(
            title="现货黄金站上5500美元",
            url="https://example.com/gold",
            source=SourceType.TOUTIAO,
            timestamp=datetime.now()
        ),
        Article(
            title="黄仁勋在CES大会发表演讲",
            url="https://example.com/jensen",
            source=SourceType.IFENG,
            timestamp=datetime.now()
        ),
    ]

    print("测试文章:")
    for i, art in enumerate(test_articles, 1):
        print(f"  {i}. {art.title}")

    print("\n执行筛选...")
    filtered = filter_by_keywords(test_articles)

    print(f"\n筛选结果: {len(filtered)}/{len(test_articles)}")
    for i, art in enumerate(filtered, 1):
        print(f"  {i}. {art.title}")


if __name__ == "__main__":
    test_filter()
