"""存储模块"""

from datetime import date
from pathlib import Path
from typing import Optional, List
import sqlite3
from contextlib import contextmanager

from ..models import Article


class TimelineDB:
    """Timeline 数据库管理（一天一个 DB）"""

    def __init__(self, db_date: Optional[date] = None):
        self.db_date = db_date or date.today()
        self.db_path = Path(f"data/db/timeline_{self.db_date.strftime('%Y-%m-%d')}.sqlite")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(self):
        """获取数据库连接（上下文管理器）"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self) -> None:
        """初始化数据库表结构"""
        with self.get_connection() as conn:
            # 检查表是否存在
            cursor = conn.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='articles'
            """)
            table_exists = cursor.fetchone() is not None

            if table_exists:
                # 检查是否有 legend 列
                cursor = conn.execute("PRAGMA table_info(articles)")
                columns = {row["name"] for row in cursor.fetchall()}
                if "legend" not in columns:
                    # 添加 legend 列（迁移旧数据库）
                    conn.execute("ALTER TABLE articles ADD COLUMN legend TEXT")
                    print("[DB] 已添加 legend 列到现有表")
            else:
                # 创建新表
                conn.execute("""
                    CREATE TABLE articles (
                        id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        url TEXT UNIQUE,
                        source TEXT NOT NULL,
                        timestamp DATETIME NOT NULL,
                        file_path TEXT,
                        tags TEXT,
                        entities TEXT,
                        legend TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                print("[DB] 已创建新表")

            # 创建索引
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_articles_timestamp
                ON articles(timestamp)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_articles_source
                ON articles(source)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_articles_legend
                ON articles(legend)
            """)
            conn.commit()

    def insert_article(self, article: Article) -> None:
        """插入文章"""
        import json

        # 处理 source - 可能是枚举或字符串
        source_value = article.source
        if hasattr(article.source, 'value'):
            source_value = article.source.value
        elif isinstance(article.source, str):
            source_value = article.source

        # 处理 timestamp - 可能是 datetime 或 date
        timestamp_value = article.timestamp
        if hasattr(timestamp_value, 'isoformat'):
            timestamp_value = timestamp_value.isoformat()
        else:
            timestamp_value = str(timestamp_value)

        with self.get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO articles
                (id, title, url, source, timestamp, file_path, tags, entities, legend)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                article.id,
                article.title,
                article.url,
                source_value,
                timestamp_value,
                article.file_path,
                json.dumps(article.tags) if article.tags else None,
                json.dumps(article.entities) if article.entities else None,
                article.legend
            ))
            conn.commit()

    def get_article(self, article_id: str) -> Optional[dict]:
        """获取单篇文章"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM articles WHERE id = ?",
                (article_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_articles(self, limit: int = 100, offset: int = 0) -> List[dict]:
        """列出文章"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM articles
                ORDER BY timestamp DESC
                LIMIT ? OFFSET ?
            """, (limit, offset))
            return [dict(row) for row in cursor.fetchall()]

    def article_exists(self, url: str) -> bool:
        """检查文章是否已存在"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT 1 FROM articles WHERE url = ?",
                (url,)
            )
            return cursor.fetchone() is not None

    def clear_all(self) -> int:
        """清空所有文章数据

        Returns:
            删除的行数
        """
        with self.get_connection() as conn:
            cursor = conn.execute("DELETE FROM articles")
            conn.commit()
            return cursor.rowcount
