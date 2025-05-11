#!/usr/bin/env python
"""
运行测试的脚本

使用方法：
    python run_tests.py          # 运行所有测试
    python run_tests.py -v       # 详细模式运行所有测试
    python run_tests.py -k api   # 只运行包含'api'的测试
"""

import sys
import os
import pytest

def main():
    """运行测试"""
    # 确保当前目录在Python路径中
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    # 设置测试环境变量
    os.environ["TESTING"] = "True"
    
    # 构建pytest参数
    args = [
        "tests",  # 测试目录
        "--cov=.",  # 覆盖率报告
        "--cov-report=term",  # 终端输出覆盖率报告
        "--cov-report=html:coverage_html",  # HTML格式覆盖率报告
    ]
    
    # 添加命令行参数
    args.extend(sys.argv[1:])
    
    # 运行测试
    return pytest.main(args)

if __name__ == "__main__":
    sys.exit(main())