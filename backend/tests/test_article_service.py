import pytest
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import article_service
from models import Category, Article, Tag


@pytest.fixture
def mock_db_session():
    """模拟数据库会话"""
    mock_session = MagicMock()
    
    # 模拟查询结果
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    
    return mock_session


def test_get_categories(mock_db_session):
    """测试获取分类列表"""
    # 模拟分类数据
    mock_categories = [
        MagicMock(spec=Category),
        MagicMock(spec=Category)
    ]
    mock_categories[0].id = 1
    mock_categories[0].name = "分类1"
    mock_categories[0].slug = "category-1"
    mock_categories[0].description = "这是分类1"
    
    mock_categories[1].id = 2
    mock_categories[1].name = "分类2"
    mock_categories[1].slug = "category-2"
    mock_categories[1].description = "这是分类2"
    
    # 设置模拟查询结果
    mock_db_session.query.return_value.all.return_value = mock_categories
    
    # 调用获取分类函数
    categories = article_service.get_categories(mock_db_session)
    
    # 验证结果
    assert len(categories) == 2
    assert categories[0]["id"] == 1
    assert categories[0]["name"] == "分类1"
    assert categories[1]["id"] == 2
    assert categories[1]["name"] == "分类2"


def test_get_article_list(mock_db_session):
    """测试获取文章列表"""
    # 模拟文章数据
    mock_articles = [
        MagicMock(spec=Article),
        MagicMock(spec=Article)
    ]
    mock_articles[0].id = 1
    mock_articles[0].title = "文章1"
    mock_articles[0].slug = "article-1"
    mock_articles[0].preview = "这是文章1的预览"
    mock_articles[0].create_time = datetime.now()
    mock_articles[0].view_count = 10
    mock_articles[0].comment_count = 5
    mock_articles[0].category = MagicMock(spec=Category)
    mock_articles[0].category.name = "分类1"
    mock_articles[0].tags = []
    
    mock_articles[1].id = 2
    mock_articles[1].title = "文章2"
    mock_articles[1].slug = "article-2"
    mock_articles[1].preview = "这是文章2的预览"
    mock_articles[1].create_time = datetime.now()
    mock_articles[1].view_count = 20
    mock_articles[1].comment_count = 8
    mock_articles[1].category = MagicMock(spec=Category)
    mock_articles[1].category.name = "分类2"
    mock_articles[1].tags = []
    
    # 设置模拟查询结果
    mock_query = mock_db_session.query.return_value
    mock_query.all.return_value = mock_articles
    mock_query.count.return_value = 2
    
    # 调用获取文章列表函数
    articles, total, total_pages = article_service.get_article_list(
        mock_db_session,
        category_id=None,
        page_size=10,
        current_page=1,
        sort_by="create_time"
    )
    
    # 验证结果
    assert len(articles) == 2
    assert articles[0]["id"] == 1
    assert articles[0]["title"] == "文章1"
    assert articles[1]["id"] == 2
    assert articles[1]["title"] == "文章2"
    assert total == 2
    assert total_pages == 1


def test_get_article_detail(mock_db_session):
    """测试获取文章详情"""
    # 模拟文章数据
    mock_article = MagicMock(spec=Article)
    mock_article.id = 1
    mock_article.title = "测试文章"
    mock_article.slug = "test-article"
    mock_article.html_content = "<h1>测试文章</h1><p>这是测试内容</p>"
    mock_article.create_time = datetime.now()
    mock_article.update_time = datetime.now()
    mock_article.view_count = 10
    mock_article.comment_count = 5
    mock_article.author = "测试作者"
    mock_article.category = MagicMock(spec=Category)
    mock_article.category.id = 1
    mock_article.category.name = "测试分类"
    mock_article.tags = []
    
    # 设置模拟查询结果
    mock_query = mock_db_session.query.return_value
    mock_query.filter.return_value.first.return_value = mock_article
    
    # 调用获取文章详情函数
    article = article_service.get_article_detail(mock_db_session, 1)
    
    # 验证结果
    assert article["id"] == 1
    assert article["title"] == "测试文章"
    assert article["content"] == "<h1>测试文章</h1><p>这是测试内容</p>"
    assert article["category"]["id"] == 1
    assert article["category"]["name"] == "测试分类"


def test_increment_view_count(mock_db_session):
    """测试增加文章阅读计数"""
    # 模拟文章数据
    mock_article = MagicMock(spec=Article)
    mock_article.id = 1
    mock_article.view_count = 10
    
    # 设置模拟查询结果
    mock_query = mock_db_session.query.return_value
    mock_query.filter.return_value.first.return_value = mock_article
    
    # 调用增加阅读计数函数
    article_service.increment_view_count(mock_db_session, 1)
    
    # 验证结果
    assert mock_article.view_count == 11
    mock_db_session.commit.assert_called_once()


def test_search_articles(mock_db_session):
    """测试搜索文章"""
    # 模拟文章数据
    mock_articles = [
        MagicMock(spec=Article),
    ]
    mock_articles[0].id = 1
    mock_articles[0].title = "测试文章"
    mock_articles[0].slug = "test-article"
    mock_articles[0].preview = "这是测试文章的预览"
    mock_articles[0].create_time = datetime.now()
    mock_articles[0].view_count = 10
    mock_articles[0].comment_count = 5
    mock_articles[0].category = MagicMock(spec=Category)
    mock_articles[0].category.name = "测试分类"
    mock_articles[0].tags = []
    
    # 设置模拟查询结果
    mock_query = mock_db_session.query.return_value
    mock_query.all.return_value = mock_articles
    mock_query.count.return_value = 1
    
    # 调用搜索文章函数
    articles, total, total_pages = article_service.search_articles(
        mock_db_session,
        keyword="测试",
        page_size=10,
        current_page=1
    )
    
    # 验证结果
    assert len(articles) == 1
    assert articles[0]["id"] == 1
    assert articles[0]["title"] == "测试文章"
    assert total == 1
    assert total_pages == 1