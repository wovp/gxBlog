from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, Boolean, func
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# 文章-标签关联表
article_tag = Table(
    'article_tag',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

# 同步状态表
class SyncStatus(Base):
    __tablename__ = "sync_status"
    
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(50), nullable=False, default="idle")  # idle, running, completed, failed
    message = Column(Text, nullable=True)
    last_sync_time = Column(DateTime, default=datetime.now)
    repo_url = Column(String(255), nullable=True)
    target_dir = Column(String(255), nullable=True)

# 分类表
class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    articles = relationship("Article", back_populates="category")

# 标签表
class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    create_time = Column(DateTime, default=datetime.now)
    
    # 关系
    articles = relationship("Article", secondary=article_tag, back_populates="tags")

# 文章表
class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False, unique=True)
    markdown_content = Column(Text, nullable=False)
    html_content = Column(Text, nullable=False)
    preview = Column(Text, nullable=True)
    author = Column(String(100), nullable=True, default="Admin")
    cover_image = Column(String(255), nullable=True)
    view_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_published = Column(Boolean, default=True)
    source_file = Column(String(255), nullable=True)  # 源文件路径
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # 关系
    category = relationship("Category", back_populates="articles")
    tags = relationship("Tag", secondary=article_tag, back_populates="articles")
    comments = relationship("Comment", back_populates="article", cascade="all, delete-orphan")

# 评论表
class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    website = Column(String(100), nullable=True)
    create_time = Column(DateTime, default=datetime.now)
    is_approved = Column(Boolean, default=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    
    # 关系
    article = relationship("Article", back_populates="comments")
    replies = relationship("Comment", backref="parent", remote_side=[id])