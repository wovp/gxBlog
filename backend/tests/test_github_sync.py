import pytest
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import github_service
from models import SyncStatus, Category, Article


@pytest.fixture
def mock_db_session():
    """模拟数据库会话"""
    mock_session = MagicMock()
    
    # 模拟查询结果
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.first.return_value = None
    
    return mock_session


@pytest.fixture
def mock_git_repo():
    """模拟Git仓库"""
    mock_repo = MagicMock()
    mock_origin = MagicMock()
    mock_repo.remotes.origin = mock_origin
    mock_origin.pull.return_value = [MagicMock()]
    return mock_repo


def test_update_sync_status(mock_db_session):
    """测试更新同步状态"""
    # 测试创建新状态记录
    github_service.update_sync_status(
        mock_db_session, 
        "running", 
        "开始同步", 
        "https://github.com/test/test.git", 
        "./test_content"
    )
    
    # 验证是否调用了add和commit
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    
    # 测试更新现有状态记录
    mock_status = MagicMock(spec=SyncStatus)
    mock_query = mock_db_session.query.return_value
    mock_query.first.return_value = mock_status
    
    github_service.update_sync_status(
        mock_db_session, 
        "completed", 
        "同步完成"
    )
    
    # 验证是否更新了状态和消息
    assert mock_status.status == "completed"
    assert mock_status.message == "同步完成"
    assert mock_db_session.commit.call_count == 2


def test_get_sync_status(mock_db_session):
    """测试获取同步状态"""
    # 测试没有同步记录的情况
    status = github_service.get_sync_status(mock_db_session)
    assert status["status"] == "idle"
    assert status["message"] == "未执行过同步"
    
    # 测试有同步记录的情况
    mock_status = MagicMock(spec=SyncStatus)
    mock_status.status = "completed"
    mock_status.message = "同步完成"
    mock_status.last_sync_time = datetime.now()
    mock_status.repo_url = "https://github.com/test/test.git"
    
    mock_query = mock_db_session.query.return_value
    mock_query.first.return_value = mock_status
    
    status = github_service.get_sync_status(mock_db_session)
    assert status["status"] == "completed"
    assert status["message"] == "同步完成"
    assert "last_sync_time" in status
    assert status["repo_url"] == "https://github.com/test/test.git"


@patch("git.Repo")
@patch("os.path.exists")
@patch("os.makedirs")
@patch.object(github_service, "process_directory")
@patch.object(github_service, "update_sync_status")
def test_sync_repository(
    mock_update_sync_status,
    mock_process_directory,
    mock_makedirs,
    mock_exists,
    mock_git_repo,
    mock_db_session
):
    """测试同步仓库功能"""
    # 模拟目录不存在，需要克隆
    mock_exists.return_value = False
    mock_git_repo.clone_from.return_value = MagicMock()
    
    # 调用同步函数
    github_service.sync_repository(
        "https://github.com/test/test.git",
        "./test_content",
        mock_db_session
    )
    
    # 验证调用
    mock_makedirs.assert_called_once_with("./test_content", exist_ok=True)
    mock_git_repo.clone_from.assert_called_once()
    mock_process_directory.assert_called_once_with("./test_content", mock_db_session)
    assert mock_update_sync_status.call_count == 2  # 开始和完成时各调用一次
    
    # 模拟目录已存在，需要拉取
    mock_exists.return_value = True
    mock_git_repo.return_value = MagicMock()
    mock_git_repo.return_value.remotes.origin.pull.return_value = [MagicMock()]
    
    # 重置模拟对象
    mock_update_sync_status.reset_mock()
    mock_process_directory.reset_mock()
    
    # 调用同步函数
    github_service.sync_repository(
        "https://github.com/test/test.git",
        "./test_content",
        mock_db_session
    )
    
    # 验证调用
    mock_git_repo.assert_called_once_with("./test_content")
    mock_git_repo.return_value.remotes.origin.pull.assert_called_once()
    mock_process_directory.assert_called_once_with("./test_content", mock_db_session)
    assert mock_update_sync_status.call_count == 2  # 开始和完成时各调用一次


@patch.object(github_service, "process_markdown_file")
@patch("os.path.isdir")
@patch("os.listdir")
def test_process_directory(
    mock_listdir,
    mock_isdir,
    mock_process_markdown_file,
    mock_db_session
):
    """测试处理目录功能"""
    # 模拟目录内容
    mock_listdir.return_value = ["file1.md", "file2.md", "subdir"]
    mock_isdir.side_effect = lambda path: "subdir" in path
    
    # 模拟分类查询
    mock_category = MagicMock(spec=Category)
    mock_category.id = 1
    mock_query = mock_db_session.query.return_value
    mock_query.filter.return_value.first.return_value = mock_category
    
    # 调用处理目录函数
    github_service.process_directory("./test_content", mock_db_session)
    
    # 验证调用
    assert mock_process_markdown_file.call_count == 2  # 处理两个markdown文件
    mock_process_markdown_file.assert_any_call(os.path.join("./test_content", "file1.md"), mock_category.id, mock_db_session)
    mock_process_markdown_file.assert_any_call(os.path.join("./test_content", "file2.md"), mock_category.id, mock_db_session)