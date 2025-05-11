from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func, or_
from typing import List, Tuple, Dict, Any, Optional
import logging
from datetime import datetime

from models import Article, Category, Tag, Comment

logger = logging.getLogger(__name__)

def get_categories(db: Session) -> List[Dict]:
    """
    获取所有分类
    """
    categories = db.query(Category).all()
    result = []
    
    for category in categories:
        # 计算该分类下的文章数量
        article_count = db.query(func.count(Article.id)).filter(Article.category_id == category.id).scalar()
        
        result.append({
            "id": category.id,  # 使用整数ID而不是字符串，匹配测试期望
            "categoryId": str(category.id),  # 保留原字段以向后兼容
            "name": category.name,
            "slug": category.slug,
            "description": category.description,
            "createTime": category.create_time.isoformat(),
            "articleCount": article_count
        })
    
    return result

def get_article_list(
    db: Session, 
    category_id: Optional[str] = None, 
    page_size: int = 10, 
    current_page: int = 1,
    sort_by: Optional[str] = None
) -> Tuple[List[Dict], int, int]:
    """
    获取文章列表
    """
    # 构建查询
    query = db.query(Article).filter(Article.is_published == True)
    
    # 如果指定了分类，则按分类筛选
    if category_id:
        query = query.filter(Article.category_id == int(category_id))
    
    # 应用排序
    if sort_by:
        if sort_by == "createTime_desc":
            query = query.order_by(desc(Article.create_time))
        elif sort_by == "createTime_asc":
            query = query.order_by(asc(Article.create_time))
        elif sort_by == "viewCount_desc":
            query = query.order_by(desc(Article.view_count))
        elif sort_by == "commentCount_desc":
            query = query.order_by(desc(Article.comment_count))
    else:
        # 默认按创建时间降序
        query = query.order_by(desc(Article.create_time))
    
    # 计算总数和总页数
    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    
    # 分页
    articles = query.offset((current_page - 1) * page_size).limit(page_size).all()
    
    # 格式化结果
    result = []
    for article in articles:
        # 获取分类信息
        category = None
        if article.category_id:
            cat = db.query(Category).filter(Category.id == article.category_id).first()
            if cat:
                category = {
                    "categoryId": str(cat.id),
                    "name": cat.name
                }
        
        result.append({
            "articleId": str(article.id),
            "title": article.title,
            "author": article.author,
            "createTime": article.create_time.isoformat(),
            "preview": article.preview,
            "viewCount": article.view_count,
            "commentCount": article.comment_count,
            "coverImage": article.cover_image,
            "category": category
        })
    
    return result, total, total_pages

def get_article_detail(db: Session, article_id: int) -> Optional[Dict]:
    """
    获取文章详情
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    
    if not article:
        return None
    
    # 获取分类信息
    category = None
    if article.category_id:
        cat = db.query(Category).filter(Category.id == article.category_id).first()
        if cat:
            category = {
                "categoryId": str(cat.id),
                "name": cat.name
            }
    
    # 获取标签
    tags = [tag.name for tag in article.tags]
    
    # 获取评论
    comments = []
    for comment in article.comments:
        if comment.is_approved:
            comments.append({
                "id": comment.id,
                "content": comment.content,
                "author": comment.author,
                "createTime": comment.create_time.isoformat()
            })
    
    return {
        "articleId": str(article.id),
        "title": article.title,
        "author": article.author,
        "createTime": article.create_time.isoformat(),
        "updateTime": article.update_time.isoformat(),
        "markdownContent": article.markdown_content,
        "htmlContent": article.html_content,
        "content": article.html_content,  # 添加content字段，匹配测试期望
        "viewCount": article.view_count,
        "commentCount": article.comment_count,
        "coverImage": article.cover_image,
        "category": category,
        "tags": tags,
        "comments": comments
    }

def increment_view_count(db: Session, article_id: int) -> None:
    """
    增加文章阅读计数
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if article:
        article.view_count += 1
        db.commit()

def search_articles(
    db: Session, 
    keyword: str, 
    page_size: int = 10, 
    current_page: int = 1
) -> Tuple[List[Dict], int, int]:
    """
    搜索文章
    """
    # 构建搜索查询
    query = db.query(Article).filter(
        Article.is_published == True,
        or_(
            Article.title.ilike(f"%{keyword}%"),
            Article.markdown_content.ilike(f"%{keyword}%"),
            Article.preview.ilike(f"%{keyword}%")
        )
    ).order_by(desc(Article.create_time))
    
    # 计算总数和总页数
    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    
    # 分页
    articles = query.offset((current_page - 1) * page_size).limit(page_size).all()
    
    # 格式化结果
    result = []
    for article in articles:
        # 获取分类信息
        category = None
        if article.category_id:
            cat = db.query(Category).filter(Category.id == article.category_id).first()
            if cat:
                category = {
                    "categoryId": str(cat.id),
                    "name": cat.name
                }
        
        result.append({
            "articleId": str(article.id),
            "title": article.title,
            "author": article.author,
            "createTime": article.create_time.isoformat(),
            "preview": article.preview,
            "viewCount": article.view_count,
            "commentCount": article.comment_count,
            "coverImage": article.cover_image,
            "category": category
        })
    
    return result, total, total_pages