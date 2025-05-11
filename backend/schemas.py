from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# 同步请求模式
class SyncRequest(BaseModel):
    repo_url: str = Field(..., description="GitHub仓库URL")
    target_dir: str = Field(..., description="目标目录路径")

# 同步响应模式
class SyncResponse(BaseModel):
    status: str
    message: str

# 同步状态模式
class SyncStatusResponse(BaseModel):
    status: str
    message: Optional[str] = None
    last_sync_time: Optional[datetime] = None
    repo_url: Optional[str] = None

# 分类模式
class Category(BaseModel):
    id: int  # 添加id字段，匹配测试期望
    categoryId: str  # 保留原字段以向后兼容
    name: str
    slug: str
    description: Optional[str] = None
    createTime: datetime
    
    class Config:
        orm_mode = True

# 标签模式
class Tag(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True

# 评论模式
class Comment(BaseModel):
    id: int
    content: str
    author: str
    createTime: datetime
    
    class Config:
        orm_mode = True

# 文章列表项模式
class ArticleListItem(BaseModel):
    articleId: str
    title: str
    author: str
    createTime: datetime
    preview: Optional[str] = None
    coverImage: Optional[str] = None
    viewCount: Optional[int] = 0
    commentCount: Optional[int] = 0
    category: Optional[Dict[str, Any]] = None
    
    class Config:
        orm_mode = True

# 文章详情模式
class ArticleDetail(BaseModel):
    articleId: str
    title: str
    author: str
    createTime: datetime
    updateTime: datetime
    markdownContent: str
    htmlContent: str
    content: str  # 添加content字段，匹配测试期望
    viewCount: int
    commentCount: int
    coverImage: Optional[str] = None
    category: Optional[Dict[str, Any]] = None
    comments: List[Comment] = []
    tags: List[str] = []
    
    class Config:
        orm_mode = True

# 分页信息模式
class Pagination(BaseModel):
    total: int
    pageSize: int
    currentPage: int
    totalPages: int

# 文章列表请求模式
class ArticleListRequest(BaseModel):
    categoryId: Optional[str] = None
    pageSize: int = 10
    currentPage: int = 1
    sortBy: Optional[str] = None  # 可以接受"create_time"、"createTime_desc"等值
    
    class Config:
        # 允许额外字段，避免验证失败
        extra = "allow"

# 文章列表响应模式
class ArticleListResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]

# 文章详情响应模式
class ArticleDetailResponse(BaseModel):
    code: int
    message: str
    data: ArticleDetail