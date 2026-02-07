"""管理后台 API

用于测试和管理数据，包括清空今日数据等操作

所有管理功能统一走 /admin/ 前缀，方便后期加权限管理
"""

from typing import Dict, Any
from fastapi import APIRouter
from datetime import date
from pathlib import Path

from ..crawlers.dedup import today_news_cache
from ..crawlers.url_cache import url_cache
from ..crawlers.source_tester import SourceTester
from ..storage.timeline_db import TimelineDB
from fastapi_cache import FastAPICache

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/cleartodaynews")
async def clear_today_data() -> Dict[str, Any]:
    """清空今日数据（数据库 + 文章文件 + 内存缓存）"""
    today = date.today()
    articles_dir = Path(f"data/articles/{today.strftime('%Y/%m/%d')}")

    deleted_files = 0
    deleted_rows = 0

    # 删除文章文件
    if articles_dir.exists():
        for file in articles_dir.glob("*.md"):
            file.unlink()
            deleted_files += 1

    # 清空数据库（使用 TimelineDB 的连接）
    db = TimelineDB(today)
    if db.db_path.exists():
        deleted_rows = db.clear_all()

    # 清空内存缓存
    print(f"[Admin] 清空前 url_cache.count={url_cache.count}, today_news_cache.count={today_news_cache.count}")
    url_cache.clear()
    today_news_cache.clear()
    print(f"[Admin] 清空后 url_cache.count={url_cache.count}, today_news_cache.count={today_news_cache.count}")

    return {
        "code": 200,
        "message": f"今日数据已清空，删除 {deleted_files} 个文章文件，清空 {deleted_rows} 条数据库记录",
        "data": {
            "date": today.isoformat(),
            "deleted_files": deleted_files,
            "deleted_rows": deleted_rows,
            "cache_count": url_cache.count
        }
    }


@router.get("/source_test")
async def test_sources() -> Dict[str, Any]:
    """测试所有新闻源，返回每个源的连接状态和数据量"""
    tester = SourceTester()
    try:
        result = await tester.test_all()
        return {
            "code": 200,
            "message": "测试完成",
            "data": result
        }
    finally:
        await tester.close()


@router.get("/cache/stats")
async def get_cache_stats() -> Dict[str, Any]:
    """获取 API 缓存统计"""
    # fastapi-cache 的 InMemoryBackend 不直接提供统计接口
    # 返回基本信息
    backend = FastAPICache.get_backend()
    return {
        "code": 200,
        "data": {
            "backend": type(backend).__name__,
            "prefix": "sfapi-cache",
            "note": "InMemoryBackend does not provide detailed stats"
        }
    }


@router.post("/cache/clear")
async def clear_api_cache() -> Dict[str, Any]:
    """清除 API 缓存"""
    # 清空所有缓存
    await FastAPICache.clear()
    return {
        "code": 200,
        "message": "已清除 API 缓存",
        "data": {"cleared": True}
    }
