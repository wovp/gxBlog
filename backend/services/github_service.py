import git
import os
import logging
import markdown
import re
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Dict, List, Tuple, Optional

from models import SyncStatus, Category, Article, Tag
# 修改导入方式，避免循环导入
from services import article_service

logger = logging.getLogger(__name__)

# 从环境变量获取黑名单配置
# 格式：逗号分隔的目录名或文件名，支持通配符
BLACKLIST_DIRS = os.getenv("BLACKLIST_DIRS", "").split(",")
BLACKLIST_FILES = os.getenv("BLACKLIST_FILES", "").split(",")
BLACKLIST_KEYWORDS = os.getenv("BLACKLIST_KEYWORDS", "").split(",")

# 清理空字符串
BLACKLIST_DIRS = [d.strip() for d in BLACKLIST_DIRS if d.strip()]
BLACKLIST_FILES = [f.strip() for f in BLACKLIST_FILES if f.strip()]
BLACKLIST_KEYWORDS = [k.strip() for k in BLACKLIST_KEYWORDS if k.strip()]

def is_blacklisted(path: str, content: str = None) -> bool:
    """
    检查路径是否在黑名单中
    """
    # 检查目录是否在黑名单中
    for blacklist_dir in BLACKLIST_DIRS:
        # 支持通配符匹配
        if re.search(blacklist_dir, path):
            logger.info(f"目录 {path} 在黑名单中，已跳过")
            return True
    
    # 检查文件是否在黑名单中
    file_name = os.path.basename(path)
    for blacklist_file in BLACKLIST_FILES:
        # 支持通配符匹配
        if re.search(blacklist_file, file_name):
            logger.info(f"文件 {file_name} 在黑名单中，已跳过")
            return True
    
    return False

def sync_repository(repo_url: str, target_dir: str, db: Session) -> None:
    """
    从GitHub拉取代码并解析文件夹结构
    """
    # 记录同步开始时间
    sync_start_time = datetime.now()
    logger.info(f"开始同步任务，时间: {sync_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 更新同步状态为运行中
        update_sync_status(db, "running", f"开始从 {repo_url} 同步数据", repo_url, target_dir)
        
        # 确保目标目录存在
        os.makedirs(target_dir, exist_ok=True)
        
        # 获取GitHub Token和代理设置（如果配置了）
        github_token = os.getenv("GITHUB_TOKEN")
        http_proxy = os.getenv("HTTP_PROXY")
        https_proxy = os.getenv("HTTPS_PROXY")
        
        # 设置Git代理环境变量
        if http_proxy or https_proxy:
            os.environ["GIT_HTTP_PROXY"] = http_proxy or ""
            os.environ["GIT_HTTPS_PROXY"] = https_proxy or ""
        
        # 如果有token，将其添加到URL中
        auth_url = repo_url
        if github_token and "https://" in repo_url:
            # 将token添加到URL中
            auth_url = repo_url.replace("https://", f"https://{github_token}@")
        
        # 检查目录是否已经是git仓库
        if os.path.exists(os.path.join(target_dir, ".git")):
            # 如果是，执行git pull
            logger.info(f"更新已存在的仓库: {target_dir}")
            repo = git.Repo(target_dir)
            
            # 如果远程URL与当前不同，更新远程URL
            if github_token and repo.remotes.origin.url != auth_url:
                repo.remotes.origin.set_url(auth_url)
                
            origin = repo.remotes.origin
            
            # 设置最大重试次数
            max_retries = 3
            retry_count = 0
            retry_delay = 5  # 初始重试延迟（秒）
            
            while retry_count < max_retries:
                try:
                    # GitPython的pull方法
                    pull_info = origin.pull()
                    logger.info("拉取更新完成")
                    break  # 成功则跳出循环
                except git.GitCommandError as e:
                    retry_count += 1
                    if "Failed to connect" in str(e) and retry_count < max_retries:
                        logger.warning(f"连接GitHub失败，正在进行第{retry_count}次重试，将在{retry_delay}秒后重试...")
                        import time
                        time.sleep(retry_delay)
                        retry_delay *= 2  # 指数退避策略
                    else:
                        logger.error(f"Git拉取命令错误: {str(e)}")
                        raise
                except Exception as e:
                    logger.error(f"拉取操作失败: {str(e)}")
                    raise
        else:
            # 如果不是，执行git clone
            logger.info(f"克隆新仓库到: {target_dir}")
            
            # 设置最大重试次数
            max_retries = 3
            retry_count = 0
            retry_delay = 5  # 初始重试延迟（秒）
            
            # 添加进度回调函数
            def progress_printer(op_code, cur_count, max_count=None, message=''):
                # 精简日志，不输出详细进度
                pass
            
            while retry_count < max_retries:
                try:
                    # GitPython的clone_from方法
                    repo = git.Repo.clone_from(
                        auth_url, 
                        target_dir, 
                        progress=progress_printer
                    )
                    logger.info("克隆完成")
                    return repo
                except git.GitCommandError as e:
                    retry_count += 1
                    if "Failed to connect" in str(e) and retry_count < max_retries:
                        logger.warning(f"连接GitHub失败，正在进行第{retry_count}次重试，将在{retry_delay}秒后重试...")
                        import time
                        time.sleep(retry_delay)
                        retry_delay *= 2  # 指数退避策略
                    else:
                        logger.error(f"Git克隆命令错误: {str(e)}")
                        raise
                except Exception as e:
                    logger.error(f"克隆操作失败: {str(e)}")
                    raise
        
        # 获取变更文件列表
        changed_files = []
        
        # 如果是已存在的仓库，获取变更文件列表
        if os.path.exists(os.path.join(target_dir, ".git")):
            try:
                repo = git.Repo(target_dir)
                # 获取最近一次拉取的变更
                # 使用git diff获取变更文件列表
                # HEAD@{1}表示上一次HEAD的位置，HEAD表示当前HEAD的位置
                diff_result = repo.git.diff("HEAD@{1}", "HEAD", name_only=True)
                
                if diff_result:
                    # 将变更文件列表转换为绝对路径
                    changed_files = [os.path.join(target_dir, file_path) for file_path in diff_result.split('\n')]
                    logger.info(f"检测到{len(changed_files)}个变更文件")
            except Exception as e:
                logger.error(f"获取变更文件列表失败: {str(e)}")
                # 如果获取变更文件列表失败，则回退到全量扫描
                logger.info("回退到全量扫描模式")
                process_directory(target_dir, db)
                return
        
        # 如果是新克隆的仓库或没有检测到变更，则进行全量扫描
        if not changed_files:
            logger.info("新仓库或没有变更，执行全量扫描")
            process_directory(target_dir, db)
        else:
            # 只处理变更的文件
            logger.info(f"开始处理{len(changed_files)}个变更文件")
            for file_path in changed_files:
                # 只处理.md文件，并且不在黑名单中
                if file_path.endswith(".md") and os.path.exists(file_path) and not is_blacklisted(file_path):
                    # 获取文件所在目录
                    dir_path = os.path.dirname(file_path)
                    # 获取目录名作为分类名
                    dir_name = os.path.basename(dir_path)
                    
                    # 如果是根目录，使用"未分类"作为分类名
                    if dir_name == os.path.basename(target_dir):
                        category_name = "未分类"
                        category_slug = "uncategorized"
                    else:
                        category_name = dir_name
                        category_slug = slugify(dir_name)
                    
                    # 检查分类是否已存在，不存在则创建
                    category = db.query(Category).filter(Category.slug == category_slug).first()
                    if not category:
                        category = Category(
                            name=category_name,
                            slug=category_slug,
                            description=f"{category_name}分类下的文章"
                        )
                        db.add(category)
                        db.commit()
                        db.refresh(category)
                    
                    # 处理Markdown文件
                    process_markdown_file(file_path, category.id, db)
        
        # 计算同步总耗时
        sync_end_time = datetime.now()
        sync_elapsed_time = (sync_end_time - sync_start_time).total_seconds()
        
        # 更新同步状态为完成
        completion_message = f"同步完成，总耗时: {sync_elapsed_time:.2f} 秒"
        logger.info(completion_message)
        update_sync_status(db, "completed", completion_message)
        
    except Exception as e:
        # 计算同步失败时的总耗时
        sync_end_time = datetime.now()
        sync_elapsed_time = (sync_end_time - sync_start_time).total_seconds()
        
        error_message = f"同步失败: {str(e)}, 耗时: {sync_elapsed_time:.2f} 秒"
        logger.error(error_message)
        
        # 记录详细错误信息
        import traceback
        logger.error(f"同步详细错误: {traceback.format_exc()}")
        
        update_sync_status(db, "failed", error_message)
        raise

def update_sync_status(db: Session, status: str, message: str, repo_url: str = None, target_dir: str = None) -> None:
    """
    更新同步状态
    """
    # 查找最新的同步状态记录
    sync_status = db.query(SyncStatus).order_by(SyncStatus.id.desc()).first()
    
    current_time = datetime.now()
    
    if sync_status:
        # 更新现有记录
        sync_status.status = status
        sync_status.message = message
        sync_status.last_sync_time = current_time
        if repo_url:
            sync_status.repo_url = repo_url
        if target_dir:
            sync_status.target_dir = target_dir
    else:
        # 创建新记录
        sync_status = SyncStatus(
            status=status,
            message=message,
            last_sync_time=current_time,
            repo_url=repo_url,
            target_dir=target_dir
        )
        db.add(sync_status)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"更新同步状态失败: {str(e)}")
        # 尝试再次创建新记录
        try:
            new_status = SyncStatus(
                status=status,
                message=f"{message} (状态更新时出错: {str(e)})",
                last_sync_time=current_time,
                repo_url=repo_url,
                target_dir=target_dir
            )
            db.add(new_status)
            db.commit()
        except Exception as inner_e:
            db.rollback()
            logger.error(f"再次尝试更新同步状态失败: {str(inner_e)}")


def get_sync_status(db: Session) -> Dict:
    """
    获取最新的同步状态
    """
    sync_status = db.query(SyncStatus).order_by(SyncStatus.id.desc()).first()
    
    if not sync_status:
        return {"status": "idle", "message": "未执行过同步"}
    
    return {
        "status": sync_status.status,
        "message": sync_status.message,
        "last_sync_time": sync_status.last_sync_time,
        "repo_url": sync_status.repo_url
    }

def process_directory(directory: str, db: Session) -> None:
    """
    处理目录，将文件夹作为分类，Markdown文件作为文章
    """
    logger.info(f"处理目录: {directory}")
    
    # 跳过.git目录和黑名单目录
    if ".git" in directory or ".ignore" in directory or directory == "" or is_blacklisted(directory):
        logger.debug(f"跳过目录: {directory}")
        return
        
    # 记录开始处理时间
    start_time = datetime.now()
    
    # 获取目录名作为分类名
    dir_name = os.path.basename(directory)
    
    # 如果是根目录，使用"未分类"作为分类名
    if dir_name == os.path.basename(os.path.dirname(directory)):
        category_name = "未分类"
        category_slug = "uncategorized"
    else:
        category_name = dir_name
        category_slug = slugify(dir_name)
    
    # 检查分类是否已存在，不存在则创建
    category = db.query(Category).filter(Category.slug == category_slug).first()
    if not category:
        category = Category(
            name=category_name,
            slug=category_slug,
            description=f"{category_name}分类下的文章"
        )
        db.add(category)
        db.commit()
        db.refresh(category)
    
    # 遍历目录中的所有文件和子目录
    items = os.listdir(directory)
    total_items = len(items)
    logger.info(f"目录 {directory} 中共有 {total_items} 个项目待处理")
    
    processed_dirs = 0
    processed_files = 0
    skipped_items = 0
    
    for index, item in enumerate(items):
        item_path = os.path.join(directory, item)
        
        # 每处理10个项目或处理到最后一个项目时输出进度
        if (index + 1) % 10 == 0 or index + 1 == total_items:
            logger.info(f"目录 {directory} 处理进度: {index + 1}/{total_items} ({(index + 1) / total_items * 100:.1f}%)")
        
        # 跳过黑名单项
        if is_blacklisted(item_path):
            skipped_items += 1
            continue
        
        if os.path.isdir(item_path):
            # 递归处理子目录
            processed_dirs += 1
            process_directory(item_path, db)
        elif item.endswith(".md"):
            # 处理Markdown文件
            processed_files += 1
            process_markdown_file(item_path, category.id, db)
    
    # 计算处理耗时
    end_time = datetime.now()
    elapsed_time = (end_time - start_time).total_seconds()
    
    logger.info(f"目录 {directory} 处理完成，耗时 {elapsed_time:.2f} 秒")
    logger.info(f"处理统计 - 子目录: {processed_dirs}，文件: {processed_files}，跳过项目: {skipped_items}")
    

def process_markdown_file(file_path: str, category_id: int, db: Session) -> None:
    """
    处理Markdown文件，提取内容并保存到数据库
    """
    
    start_time = datetime.now()
    logger.debug(f"开始处理文件: {file_path}")
    
    try:
        # 读取文件内容
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        file_size = os.path.getsize(file_path) / 1024  # KB
        logger.debug(f"文件大小: {file_size:.2f} KB, 内容长度: {len(content)} 字符")
        
        # 检查文件路径是否在黑名单中
        if is_blacklisted(file_path):
            return
        
        # 提取标题（使用第一个#标记的行作为标题）
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            # 如果没有找到标题，使用文件名作为标题
            title = os.path.splitext(os.path.basename(file_path))[0]
        
        # 生成slug
        slug = slugify(title)
        
        # 提取预览（使用前200个字符作为预览）
        preview = re.sub(r'^#\s+.+$', '', content, 1, re.MULTILINE).strip()[:200] + "..."
        
        # 将Markdown转换为HTML - 已注释，不再转换为HTML
        # html_content = markdown.markdown(
        #     content,
        #     extensions=['extra', 'codehilite', 'tables', 'toc']
        # )
        
        # 不进行HTML转换，直接使用原始Markdown内容
        html_content = ""  # 或者设置为空字符串: html_content = ""
        
        # 提取标签（使用文件中的#标签格式）
        tags = []
        tag_matches = re.findall(r'#(\w+)', content)
        for tag_name in tag_matches:
            if len(tag_name) > 2:  # 忽略太短的标签
                tag = db.query(Tag).filter(Tag.name == tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.add(tag)
                    db.commit()
                    db.refresh(tag)
                tags.append(tag)
        
        # 检查文章是否已存在（通过slug判断）
        article = db.query(Article).filter(Article.slug == slug).first()
        
        if article:
            # 更新现有文章
            article.title = title
            article.markdown_content = content
            article.html_content = html_content
            article.preview = preview
            article.update_time = datetime.now()
            article.source_file = file_path
            article.category_id = category_id
            article.tags = tags
        else:
            # 创建新文章
            article = Article(
                title=title,
                slug=slug,
                markdown_content=content,
                html_content=html_content,
                preview=preview,
                source_file=file_path,
                category_id=category_id
            )
            article.tags = tags
            db.add(article)
        
        db.commit()
        
        # 计算处理耗时
        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()
        logger.debug(f"文件 {file_path} 处理完成，耗时 {elapsed_time:.2f} 秒")
        
    except Exception as e:
        logger.error(f"处理文件 {file_path} 失败: {str(e)}")
        db.rollback()
        
        # 记录详细错误信息
        import traceback
        logger.error(f"处理文件详细错误: {traceback.format_exc()}")
        

def slugify(text: str) -> str:
    """
    将文本转换为URL友好的slug格式
    """
    # 转换为小写
    text = text.lower()
    # 移除非字母数字字符
    text = re.sub(r'[^\w\s-]', '', text)
    # 将空格替换为连字符
    text = re.sub(r'[\s]+', '-', text.strip())
    return text