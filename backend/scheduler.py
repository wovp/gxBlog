from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
import logging
import os
import git
from dotenv import load_dotenv

from database import SessionLocal
from services import github_service

# 加载环境变量
load_dotenv()

# 配置日志
logger = logging.getLogger(__name__)

# 获取环境变量
GITHUB_REPO_URL = os.getenv("GITHUB_REPO_URL")
GITHUB_TARGET_DIR = os.getenv("GITHUB_TARGET_DIR")
SYNC_INTERVAL = os.getenv("SYNC_INTERVAL", "0 */6 * * *")  # 默认每6小时同步一次

def sync_job():
    """
    定时同步任务
    """
    logger.info("开始执行定时同步任务")
    
    if not GITHUB_REPO_URL or not GITHUB_TARGET_DIR:
        logger.error("未配置GitHub仓库URL或目标目录，无法执行同步任务")
        return
    
    logger.info(f"同步配置 - 仓库URL: {GITHUB_REPO_URL}, 目标目录: {GITHUB_TARGET_DIR}")
    
    try:
        # 创建数据库会话
        db = SessionLocal()
        try:
            # 执行同步
            logger.info("开始调用sync_repository函数")
            github_service.sync_repository(
                repo_url=GITHUB_REPO_URL,
                target_dir=GITHUB_TARGET_DIR,
                db=db
            )
            logger.info("定时同步任务执行成功")
        except git.GitCommandError as e:
            logger.error(f"Git命令执行错误: {str(e)}")
            logger.error(f"Git错误详情 - 命令: {e.command}, 状态: {e.status}, 标准输出: {e.stdout}, 标准错误: {e.stderr}")
        except TimeoutError as e:
            logger.error(f"Git操作超时: {str(e)}")
        except Exception as e:
            logger.error(f"定时同步任务执行失败: {str(e)}")
            # 打印详细的异常堆栈信息
            import traceback
            logger.error(f"异常堆栈: {traceback.format_exc()}")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"创建数据库会话失败: {str(e)}")
        import traceback
        logger.error(f"数据库会话异常堆栈: {traceback.format_exc()}")

def start_scheduler():
    """
    启动定时任务调度器
    """
    scheduler = BackgroundScheduler()
    
    # 添加定时同步任务
    scheduler.add_job(
        sync_job,
        CronTrigger.from_crontab(SYNC_INTERVAL),  # 使用cron表达式配置定时
        id="github_sync_job",
        replace_existing=True
    )
    
    # 启动调度器
    scheduler.start()
    logger.info(f"定时任务调度器已启动，同步间隔: {SYNC_INTERVAL}")
    
    # 立即执行一次同步任务（使用后台线程，避免阻塞应用启动）
    logger.info("应用启动时立即执行一次同步任务（后台执行）")
    import threading
    sync_thread = threading.Thread(target=sync_job)
    sync_thread.daemon = True  # 设置为守护线程，应用关闭时自动结束
    sync_thread.start()
    
    return scheduler