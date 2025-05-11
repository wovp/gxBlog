from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import git
import markdown
import logging
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel

# 加载环境变量
load_dotenv()

# 导入自定义模块
from database import get_db, engine
import models
import schemas
from services import github_service, article_service

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 配置日志使用UTF-8编码
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="博客API", description="从GitHub拉取Markdown文件并提供博客API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置为具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查端点
@app.get("/")
def read_root():
    return {"status": "ok", "message": "博客API服务正常运行"}

# 从GitHub拉取代码并解析
@app.post("/api/sync", response_model=schemas.SyncResponse)
def sync_from_github(task: schemas.SyncRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        # 将同步任务放入后台执行，避免请求超时
        background_tasks.add_task(
            github_service.sync_repository,
            repo_url=task.repo_url,
            target_dir=task.target_dir,
            db=db
        )
        return {"status": "started", "message": "同步任务已开始，请稍后查询结果"}
    except Exception as e:
        logger.error(f"同步任务启动失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"同步任务启动失败: {str(e)}")

# 获取同步状态
@app.get("/api/sync/status")
def get_sync_status(db: Session = Depends(get_db)):
    status = github_service.get_sync_status(db)
    return status

# 获取所有分类
@app.get("/api/category", response_model=List[schemas.Category])
def get_categories(db: Session = Depends(get_db)):
    categories = article_service.get_categories(db)
    return categories

# 获取文章列表
@app.post("/api/article/list", response_model=schemas.ArticleListResponse)
def get_article_list(
    request: schemas.ArticleListRequest,
    db: Session = Depends(get_db)
):
    articles, total, total_pages = article_service.get_article_list(
        db=db,
        category_id=request.categoryId,
        page_size=request.pageSize,
        current_page=request.currentPage,
        sort_by=request.sortBy
    )
    
    return {
        "code": 200,
        "message": "成功",
        "data": {
            "list": articles,
            "pagination": {
                "total": total,
                "pageSize": request.pageSize,
                "currentPage": request.currentPage,
                "totalPages": total_pages
            }
        }
    }

# 获取文章详情
@app.get("/api/article/{article_id}", response_model=schemas.ArticleDetailResponse)
def get_article_detail(article_id: int, db: Session = Depends(get_db)):
    article = article_service.get_article_detail(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 增加阅读计数
    article_service.increment_view_count(db, article_id)
    
    return {
        "code": 200,
        "message": "成功",
        "data": article
    }

# 搜索文章请求模型
class SearchArticlesRequest(BaseModel):
    keyword: str
    pageSize: int = 10
    currentPage: int = 1
    
    class Config:
        # 允许额外字段，避免验证失败
        extra = "allow"

# 搜索文章
@app.get("/api/article/search", response_model=schemas.ArticleListResponse)
def search_articles(
    request: SearchArticlesRequest = Depends(),
    db: Session = Depends(get_db)
):
    articles, total, total_pages = article_service.search_articles(
        db=db,
        keyword=request.keyword,
        page_size=request.pageSize,
        current_page=request.currentPage
    )
    
    return {
        "code": 200,
        "message": "成功",
        "data": {
            "list": articles,
            "pagination": {
                "total": total,
                "pageSize": request.pageSize,
                "currentPage": request.currentPage,
                "totalPages": total_pages
            }
        }
    }

# 启动定时任务调度器
from scheduler import start_scheduler

@app.on_event("startup")
def startup_event():
    """应用启动时执行"""
    # 启动定时任务调度器
    scheduler = start_scheduler()
    # 将调度器保存到应用状态中，以便在需要时访问
    app.state.scheduler = scheduler
    logger.info("应用启动，定时任务调度器已初始化")

@app.on_event("shutdown")
def shutdown_event():
    """应用关闭时执行"""
    # 关闭调度器
    if hasattr(app.state, "scheduler"):
        app.state.scheduler.shutdown()
        logger.info("应用关闭，定时任务调度器已停止")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)