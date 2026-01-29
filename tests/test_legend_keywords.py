"""测试 legend 关键词筛选功能"""

import pytest
from src.crawlers.keywords_filter import filter_by_keywords, _load_keywords
from src.models import Article, SourceType
from src.storage.timeline_db import TimelineDB
from datetime import datetime


class TestLoadKeywords:
    """测试关键词加载功能"""

    def test_load_keywords_structure(self):
        """验证 keywords 加载后的结构"""
        result = _load_keywords()

        assert isinstance(result, dict), "返回值应该是 dict"
        assert "legend" in result, "应包含 legend 键"
        assert "front" in result, "应包含 front 键"
        assert isinstance(result["legend"], dict), "legend 应该是 dict"
        assert isinstance(result["front"], list), "front 应该是 list"

    def test_load_legend_keywords(self):
        """验证 legend 关键词正确展平"""
        result = _load_keywords()

        # 检查 musk 关键词
        assert "musk" in result["legend"], "应包含 musk"
        musk_keywords = result["legend"]["musk"]
        assert isinstance(musk_keywords, list), "musk 关键词应该是 list"
        assert len(musk_keywords) > 0, "musk 应该有关键词"
        # 验证一些预期关键词存在
        assert "马斯克" in musk_keywords, "应包含'马斯克'"
        assert "特斯拉" in musk_keywords, "应包含'特斯拉'"

        # 检查 huang 关键词
        assert "huang" in result["legend"], "应包含 huang"
        huang_keywords = result["legend"]["huang"]
        assert "黄仁勋" in huang_keywords, "应包含'黄仁勋'"
        assert "英伟达" in huang_keywords, "应包含'英伟达'"

        # 检查 altman 关键词
        assert "altman" in result["legend"], "应包含 altman"
        altman_keywords = result["legend"]["altman"]
        assert "OpenAI" in altman_keywords, "应包含'OpenAI'"

    def test_load_front_keywords(self):
        """验证 front 关键词正确展平"""
        result = _load_keywords()

        front_keywords = result["front"]
        assert isinstance(front_keywords, list), "front 关键词应该是 list"
        assert len(front_keywords) > 0, "front 应该有关键词"

        # 验证一些预期关键词存在
        assert "AGI" in front_keywords, "应包含'AGI'"
        assert "deepseek" in front_keywords, "应包含'deepseek'"
        assert "人形机器人" in front_keywords, "应包含'人形机器人'"


class TestLegendMatching:
    """测试 legend 匹配功能"""

    def test_match_legend_musk(self):
        """马斯克相关新闻正确标注"""
        articles = [
            Article(
                title="马斯克宣布星舰最新发射计划",
                url="https://example.com/spacex-starship",
                source=SourceType.IFENG,
                timestamp=datetime.now()
            ),
            Article(
                title="特斯拉FSD在中国推出",
                url="https://example.com/tesla-fsd",
                source=SourceType.TOUTIAO,
                timestamp=datetime.now()
            ),
        ]

        filtered = filter_by_keywords(articles)

        assert len(filtered) == 2, "应该匹配2篇文章"
        assert filtered[0].legend == "musk", "第一篇文章应该是 musk"
        assert filtered[1].legend == "musk", "第二篇文章应该是 musk"

    def test_match_legend_huang(self):
        """黄仁勋相关新闻正确标注"""
        articles = [
            Article(
                title="黄仁勋在CES大会发表演讲",
                url="https://example.com/jensen",
                source=SourceType.IFENG,
                timestamp=datetime.now()
            ),
            Article(
                title="英伟达发布新一代AI芯片H200",
                url="https://example.com/nvidia-h200",
                source=SourceType.TOUTIAO,
                timestamp=datetime.now()
            ),
        ]

        filtered = filter_by_keywords(articles)

        assert len(filtered) == 2, "应该匹配2篇文章"
        assert filtered[0].legend == "huang", "第一篇文章应该是 huang"
        assert filtered[1].legend == "huang", "第二篇文章应该是 huang"

    def test_match_legend_altman(self):
        """奥尔特曼相关新闻正确标注"""
        articles = [
            Article(
                title="Sam Altman宣布OpenAI新计划",
                url="https://example.com/openai",
                source=SourceType.IFENG,
                timestamp=datetime.now()
            ),
            Article(
                title="ChatGPT迎来重大更新",
                url="https://example.com/chatgpt",
                source=SourceType.TOUTIAO,
                timestamp=datetime.now()
            ),
        ]

        filtered = filter_by_keywords(articles)

        assert len(filtered) == 2, "应该匹配2篇文章"
        assert filtered[0].legend == "altman", "第一篇文章应该是 altman"
        assert filtered[1].legend == "altman", "第二篇文章应该是 altman"


class TestFrontMatching:
    """测试 front 匹配功能"""

    def test_match_front(self):
        """前沿资讯正确标注"""
        # 使用不与 legend 交叉的测试数据
        articles = [
            Article(
                title="中国大模型deepseek发布新版本",
                url="https://example.com/deepseek",
                source=SourceType.TOUTIAO,
                timestamp=datetime.now()
            ),
            Article(
                title="具身智能领域迎来新突破",  # 使用"具身智能"而非"人形机器人"（与musk的"机器人"不交叉）
                url="https://example.com/robot",
                source=SourceType.IFENG,
                timestamp=datetime.now()
            ),
        ]

        filtered = filter_by_keywords(articles)

        assert len(filtered) == 2, "应该匹配2篇文章"
        assert filtered[0].legend is None, "第一篇文章应该是 front (legend=None)"
        assert filtered[1].legend is None, "第二篇文章应该是 front (legend=None)"

    def test_legend_priority_over_front(self):
        """legend 和 front 都命中时 legend 优先"""
        # "大模型" 在 front 关键词中，但"马斯克"在 legend 中
        articles = [
            Article(
                title="马斯克谈大模型发展前景",
                url="https://example.com/musk-ai",
                source=SourceType.IFENG,
                timestamp=datetime.now()
            ),
        ]

        filtered = filter_by_keywords(articles)

        assert len(filtered) == 1, "应该匹配1篇文章"
        assert filtered[0].legend == "musk", "应优先匹配 legend (musk)，而非 front"


class TestFiltering:
    """测试过滤功能"""

    def test_no_match_filtered_out(self):
        """都不匹配的新闻被过滤掉"""
        articles = [
            Article(
                title="日经225指数低开0.2%",
                url="https://example.com/finance",
                source=SourceType.TOUTIAO,
                timestamp=datetime.now()
            ),
            Article(
                title="现货黄金站上5500美元",
                url="https://example.com/gold",
                source=SourceType.TOUTIAO,
                timestamp=datetime.now()
            ),
        ]

        filtered = filter_by_keywords(articles)

        assert len(filtered) == 0, "不相关的文章应该被过滤掉"

    def test_case_insensitive(self):
        """大小写不敏感匹配"""
        articles = [
            Article(
                title="NVIDIA发布新GPU",  # 大写
                url="https://example.com/nvidia",
                source=SourceType.IFENG,
                timestamp=datetime.now()
            ),
            Article(
                title="nvidia在中国推出新产品",  # 小写
                url="https://example.com/nvidia2",
                source=SourceType.TOUTIAO,
                timestamp=datetime.now()
            ),
            Article(
                title="英伟达CEO黄仁勋发表演讲",  # 中文
                url="https://example.com/jensen",
                source=SourceType.IFENG,
                timestamp=datetime.now()
            ),
        ]

        filtered = filter_by_keywords(articles)

        assert len(filtered) == 3, "大小写不敏感，应该全部匹配"
        assert all(a.legend == "huang" for a in filtered), "都应该标注为 huang"


class TestArticleModel:
    """测试 Article 模型"""

    def test_article_model_has_legend(self):
        """Article 模型包含 legend 字段"""
        article = Article(
            title="测试新闻",
            url="https://example.com/test",
            source=SourceType.IFENG,
            timestamp=datetime.now()
        )

        # 默认值应该是 None
        assert hasattr(article, 'legend'), "Article 应该有 legend 属性"
        assert article.legend is None, "默认 legend 应该是 None"

        # 可以设置 legend
        article.legend = "musk"
        assert article.legend == "musk", "可以设置 legend 值"

    def test_article_with_legend_in_init(self):
        """初始化时设置 legend"""
        article = Article(
            title="马斯克相关新闻",
            url="https://example.com/musk",
            source=SourceType.IFENG,
            timestamp=datetime.now(),
            legend="musk"
        )

        assert article.legend == "musk", "初始化时设置的 legend 应生效"


class TestDatabase:
    """测试数据库"""

    def test_db_has_legend_column(self, test_db):
        """数据库表包含 legend 列"""
        db = test_db

        # 使用 PRAGMA 检查表结构
        with db.get_connection() as conn:
            cursor = conn.execute("PRAGMA table_info(articles)")
            columns = [row["name"] for row in cursor.fetchall()]

        assert "legend" in columns, "articles 表应该包含 legend 列"

    def test_db_legend_index(self, test_db):
        """legend 索引存在"""
        db = test_db

        # 使用 PRAGMA 检查索引
        with db.get_connection() as conn:
            cursor = conn.execute("PRAGMA index_list('articles')")
            indexes = [row["name"] for row in cursor.fetchall()]

        assert "idx_articles_legend" in indexes, "应该存在 idx_articles_legend 索引"

    def test_insert_article_with_legend(self, test_db):
        """插入带 legend 的文章"""
        db = test_db

        article = Article(
            title="马斯克宣布星舰发射计划",
            url="https://example.com/starship",
            source=SourceType.IFENG,
            timestamp=datetime.now(),
            legend="musk"
        )

        db.insert_article(article)

        # 查询验证
        retrieved = db.get_article(article.id)
        assert retrieved is not None, "应该能查询到插入的文章"
        assert retrieved["legend"] == "musk", "legend 字段应该正确保存"

    def test_query_by_legend(self, test_db):
        """按 legend 查询文章"""
        db = test_db

        # 插入不同 legend 的文章
        articles = [
            Article(
                title="马斯克新闻",
                url="https://example.com/musk1",
                source=SourceType.IFENG,
                timestamp=datetime.now(),
                legend="musk"
            ),
            Article(
                title="黄仁勋新闻",
                url="https://example.com/huang1",
                source=SourceType.IFENG,
                timestamp=datetime.now(),
                legend="huang"
            ),
            Article(
                title="前沿资讯",
                url="https://example.com/front1",
                source=SourceType.IFENG,
                timestamp=datetime.now(),
                legend=None
            ),
        ]

        for article in articles:
            db.insert_article(article)

        # 查询 legend=musk 的文章
        with db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM articles WHERE legend = ?",
                ("musk",)
            )
            musk_articles = [dict(row) for row in cursor.fetchall()]

        assert len(musk_articles) == 1, "应该查询到1篇 musk 文章"
        assert musk_articles[0]["title"] == "马斯克新闻"

        # 查询 legend IS NULL 的文章
        with db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM articles WHERE legend IS NULL"
            )
            front_articles = [dict(row) for row in cursor.fetchall()]

        assert len(front_articles) == 1, "应该查询到1篇 front 文章"
        assert front_articles[0]["title"] == "前沿资讯"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
