import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
import sys
import json
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Base, get_db
from main import app
import models

# 创建内存数据库用于测试
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 测试数据
test_category = {
    "name": "测试分类",
    "slug": "test-category",
    "description": "这是一个测试分类"
}

test_article = {
    "title": "测试文章",
    "slug": "test-article",
    "markdown_content": "# 测试文章\n这是一个测试文章的内容",
    "html_content": "<h1>测试文章</h1>\n<p>这是一个测试文章的内容</p>",
    "preview": "这是一个测试文章的内容...",
    "author": "测试作者",
    "is_published": True
}


@pytest.fixture(scope="module")
def client():
    # 创建测试数据库表
    Base.metadata.create_all(bind=engine)
    
    # 覆盖依赖项
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    # 创建测试客户端
    with TestClient(app) as test_client:
        yield test_client
    
    # 清理
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def db_session():
    # 创建测试数据库表
    Base.metadata.create_all(bind=engine)
    
    # 创建会话
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    
    # 清理
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def test_data(db_session):
    # 创建测试分类
    category = models.Category(
        name=test_category["name"],
        slug=test_category["slug"],
        description=test_category["description"]
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    
    # 创建测试文章
    article = models.Article(
        title=test_article["title"],
        slug=test_article["slug"],
        markdown_content=test_article["markdown_content"],
        html_content=test_article["html_content"],
        preview=test_article["preview"],
        author=test_article["author"],
        is_published=test_article["is_published"],
        category_id=category.id
    )
    db_session.add(article)
    db_session.commit()
    db_session.refresh(article)
    
    # 创建同步状态记录
    sync_status = models.SyncStatus(
        status="completed",
        message="测试同步完成",
        last_sync_time=datetime.now(),
        repo_url="https://github.com/test/test.git",
        target_dir="./test_content"
    )
    db_session.add(sync_status)
    db_session.commit()
    
    return {"category": category, "article": article}


def test_read_root(client):
    """测试健康检查端点"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_get_categories(client, test_data):
    """测试获取分类列表"""
    response = client.get("/api/category")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["name"] == test_category["name"]
    assert response.json()[0]["slug"] == test_category["slug"]


def test_get_article_list(client, test_data):
    """测试获取文章列表"""
    response = client.post(
        "/api/article/list",
        json={
            "categoryId": test_data["category"].id,
            "pageSize": 10,
            "currentPage": 1,
            "sortBy": "create_time"
        }
    )
    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert len(response.json()["data"]["list"]) >= 1
    assert response.json()["data"]["list"][0]["title"] == test_article["title"]


def test_get_article_detail(client, test_data):
    """测试获取文章详情"""
    response = client.get(f"/api/article/{test_data['article'].id}")
    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert response.json()["data"]["title"] == test_article["title"]
    assert response.json()["data"]["content"] == test_article["html_content"]


def test_search_articles(client, test_data):
    """测试搜索文章"""
    response = client.get(
        "/api/article/search",
        params={"keyword": "测试", "pageSize": 10, "currentPage": 1}
    )
    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert len(response.json()["data"]["list"]) >= 1


def test_get_sync_status(client):
    """测试获取同步状态"""
    response = client.get("/api/sync/status")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "message" in response.json()


def test_article_not_found(client):
    """测试获取不存在的文章"""
    response = client.get("/api/article/9999")
    assert response.status_code == 404
    assert "文章不存在" in response.json()["detail"]