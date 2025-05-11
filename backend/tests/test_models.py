import pytest
import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from models import SyncStatus, Category, Article, Tag, Comment, article_tag

# 创建内存数据库用于测试
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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


def test_sync_status_model(db_session):
    """测试同步状态模型"""
    # 创建同步状态记录
    sync_status = SyncStatus(
        status="running",
        message="测试同步中",
        last_sync_time=datetime.now(),
        repo_url="https://github.com/test/test.git",
        target_dir="./test_content"
    )
    db_session.add(sync_status)
    db_session.commit()
    
    # 查询并验证
    result = db_session.query(SyncStatus).filter(SyncStatus.status == "running").first()
    assert result is not None
    assert result.status == "running"
    assert result.message == "测试同步中"
    assert result.repo_url == "https://github.com/test/test.git"
    assert result.target_dir == "./test_content"


def test_category_model(db_session):
    """测试分类模型"""
    # 创建分类记录
    category = Category(
        name="测试分类",
        slug="test-category",
        description="这是一个测试分类"
    )
    db_session.add(category)
    db_session.commit()
    
    # 查询并验证
    result = db_session.query(Category).filter(Category.slug == "test-category").first()
    assert result is not None
    assert result.name == "测试分类"
    assert result.description == "这是一个测试分类"


def test_tag_model(db_session):
    """测试标签模型"""
    # 创建标签记录
    tag = Tag(
        name="测试标签"
    )
    db_session.add(tag)
    db_session.commit()
    
    # 查询并验证
    result = db_session.query(Tag).filter(Tag.name == "测试标签").first()
    assert result is not None
    assert result.name == "测试标签"


def test_article_model(db_session):
    """测试文章模型"""
    # 创建分类
    category = Category(
        name="测试分类",
        slug="test-category",
        description="这是一个测试分类"
    )
    db_session.add(category)
    db_session.commit()
    
    # 创建标签
    tag1 = Tag(name="标签1")
    tag2 = Tag(name="标签2")
    db_session.add_all([tag1, tag2])
    db_session.commit()
    
    # 创建文章
    article = Article(
        title="测试文章",
        slug="test-article",
        markdown_content="# 测试文章\n这是测试内容",
        html_content="<h1>测试文章</h1><p>这是测试内容</p>",
        preview="这是测试内容...",
        author="测试作者",
        category_id=category.id
    )
    article.tags = [tag1, tag2]
    db_session.add(article)
    db_session.commit()
    
    # 查询并验证
    result = db_session.query(Article).filter(Article.slug == "test-article").first()
    assert result is not None
    assert result.title == "测试文章"
    assert result.author == "测试作者"
    assert result.category_id == category.id
    assert len(result.tags) == 2
    assert result.tags[0].name in ["标签1", "标签2"]
    assert result.tags[1].name in ["标签1", "标签2"]


def test_comment_model(db_session):
    """测试评论模型"""
    # 创建分类
    category = Category(
        name="测试分类",
        slug="test-category",
        description="这是一个测试分类"
    )
    db_session.add(category)
    db_session.commit()
    
    # 创建文章
    article = Article(
        title="测试文章",
        slug="test-article",
        markdown_content="# 测试文章\n这是测试内容",
        html_content="<h1>测试文章</h1><p>这是测试内容</p>",
        preview="这是测试内容...",
        author="测试作者",
        category_id=category.id
    )
    db_session.add(article)
    db_session.commit()
    
    # 创建评论
    comment = Comment(
        content="这是一条测试评论",
        author="评论者",
        email="test@example.com",
        website="https://example.com",
        article_id=article.id
    )
    db_session.add(comment)
    db_session.commit()
    
    # 创建回复评论
    reply = Comment(
        content="这是一条回复评论",
        author="回复者",
        email="reply@example.com",
        article_id=article.id,
        parent_id=comment.id
    )
    db_session.add(reply)
    db_session.commit()
    
    # 查询并验证评论
    result = db_session.query(Comment).filter(Comment.author == "评论者").first()
    assert result is not None
    assert result.content == "这是一条测试评论"
    assert result.article_id == article.id
    
    # 查询并验证回复
    result = db_session.query(Comment).filter(Comment.author == "回复者").first()
    assert result is not None
    assert result.content == "这是一条回复评论"
    assert result.parent_id == comment.id
    
    # 验证文章的评论数
    article = db_session.query(Article).filter(Article.id == article.id).first()
    assert len(article.comments) == 2


def test_relationships(db_session):
    """测试模型之间的关系"""
    # 创建分类
    category = Category(
        name="测试分类",
        slug="test-category",
        description="这是一个测试分类"
    )
    db_session.add(category)
    db_session.commit()
    
    # 创建标签
    tag = Tag(name="测试标签")
    db_session.add(tag)
    db_session.commit()
    
    # 创建文章
    article = Article(
        title="测试文章",
        slug="test-article",
        markdown_content="# 测试文章\n这是测试内容",
        html_content="<h1>测试文章</h1><p>这是测试内容</p>",
        preview="这是测试内容...",
        author="测试作者",
        category_id=category.id
    )
    article.tags = [tag]
    db_session.add(article)
    db_session.commit()
    
    # 创建评论
    comment = Comment(
        content="这是一条测试评论",
        author="评论者",
        email="test@example.com",
        article_id=article.id
    )
    db_session.add(comment)
    db_session.commit()
    
    # 验证分类-文章关系
    category = db_session.query(Category).filter(Category.id == category.id).first()
    assert len(category.articles) == 1
    assert category.articles[0].title == "测试文章"
    
    # 验证文章-分类关系
    article = db_session.query(Article).filter(Article.id == article.id).first()
    assert article.category.name == "测试分类"
    
    # 验证文章-标签关系
    assert len(article.tags) == 1
    assert article.tags[0].name == "测试标签"
    
    # 验证标签-文章关系
    tag = db_session.query(Tag).filter(Tag.id == tag.id).first()
    assert len(tag.articles) == 1
    assert tag.articles[0].title == "测试文章"
    
    # 验证文章-评论关系
    assert len(article.comments) == 1
    assert article.comments[0].content == "这是一条测试评论"
    
    # 验证评论-文章关系
    comment = db_session.query(Comment).filter(Comment.id == comment.id).first()
    assert comment.article.title == "测试文章"