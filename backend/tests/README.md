# FastAPI博客后端测试

本目录包含了FastAPI博客后端的测试用例，使用pytest框架进行测试。

## 测试内容

测试用例覆盖了以下功能：

1. **API测试**：测试所有API端点的功能
   - 健康检查
   - 获取分类列表
   - 获取文章列表
   - 获取文章详情
   - 搜索文章
   - 获取同步状态

2. **GitHub同步测试**：测试GitHub同步功能
   - 更新同步状态
   - 获取同步状态
   - 同步仓库
   - 处理目录

3. **文章服务测试**：测试文章相关服务
   - 获取分类
   - 获取文章列表
   - 获取文章详情
   - 增加阅读计数
   - 搜索文章

## 运行测试

### 安装测试依赖

```bash
pip install -r requirements-test.txt
```

### 运行所有测试

```bash
python run_tests.py
```

### 运行特定测试

```bash
python run_tests.py -k api  # 只运行包含'api'的测试
python run_tests.py -k test_get_article_list  # 只运行特定测试函数
python run_tests.py tests/test_api.py  # 只运行特定测试文件
```

### 查看详细输出

```bash
python run_tests.py -v
```

### 查看测试覆盖率报告

运行测试后，会生成覆盖率报告：

- 终端输出覆盖率摘要
- `coverage_html`目录中包含详细的HTML格式覆盖率报告

## 测试结构

- `conftest.py`：测试配置和共享fixture
- `test_api.py`：API端点测试
- `test_github_sync.py`：GitHub同步功能测试
- `test_article_service.py`：文章服务功能测试