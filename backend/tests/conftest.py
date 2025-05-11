import os
import sys
import pytest
from pathlib import Path

# 确保测试可以导入主应用模块
sys.path.append(str(Path(__file__).parent.parent))

# 设置测试环境变量
os.environ["TESTING"] = "True"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["GITHUB_REPO_URL"] = "https://github.com/test/test.git"
os.environ["GITHUB_TARGET_DIR"] = "./test_content"
os.environ["SYNC_INTERVAL"] = "0 */6 * * *"

# 如果需要代理，可以在这里设置
# os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
# os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """设置测试环境"""
    # 创建测试内容目录
    os.makedirs("./test_content", exist_ok=True)
    
    yield
    
    # 清理测试内容目录
    if os.path.exists("./test_content"):
        import shutil
        shutil.rmtree("./test_content")