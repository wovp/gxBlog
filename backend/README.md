# 博客后端API

这是一个基于FastAPI的博客后端API，用于从GitHub拉取Markdown文件，解析为文章并存储到MySQL数据库中，为前端提供API接口。

## 功能特点

- 自动定时从GitHub仓库拉取代码
- 解析文件夹结构，将目录作为分类
- 解析Markdown文件作为文章内容
- 提供RESTful API接口
- 支持文章分类、标签、评论等功能
- 支持文章搜索

## 环境要求

- Python 3.8+
- MySQL 5.7+

## 安装步骤

1. 克隆项目

```bash
git clone <项目地址>
cd backend
```

2. 创建虚拟环境并安装依赖

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. 配置环境变量

复制`.env.example`文件为`.env`，并根据实际情况修改配置：

```bash
cp .env.example .env
# 编辑.env文件，设置数据库连接信息和GitHub仓库信息
```

主要配置项：
- 数据库连接信息（DB_USER, DB_PASSWORD等）
- GitHub仓库URL（GITHUB_REPO_URL）
- 本地目标目录（GITHUB_TARGET_DIR）
- 同步时间间隔（SYNC_INTERVAL，使用cron表达式）
- 网络代理设置：HTTP_PROXY, HTTPS_PROXY（如果需要通过代理访问GitHub）

4. 初始化数据库

确保MySQL服务已启动，并创建了对应的数据库：

```sql
CREATE DATABASE gxblog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. 启动服务

```bash
uvicorn main:app --reload
```

服务将在 http://localhost:8000 运行，API文档可访问 http://localhost:8000/docs

## API接口

### 同步GitHub仓库

- POST `/api/sync`：从GitHub拉取代码并解析
- GET `/api/sync/status`：获取同步状态

### 分类管理

- GET `/api/category`：获取所有分类

### 文章管理

- POST `/api/article/list`：获取文章列表
- GET `/api/article/{article_id}`：获取文章详情
- GET `/api/article/search`：搜索文章

## 与前端集成

本后端API设计与前端Vue项目的接口保持一致，可以直接替换前端项目中的Mock数据，实现真实的数据交互。

## 注意事项

- 应用启动后会根据配置的时间间隔自动从GitHub拉取文章数据
- 也可以通过API手动触发同步操作
- 文章的Markdown格式应符合一定规范，建议使用标准的Markdown语法
- 默认情况下，文件夹名称将作为分类名称，Markdown文件的第一个标题将作为文章标题

## 定时同步配置

定时同步功能使用cron表达式配置，默认为每6小时同步一次（`0 */6 * * *`）。

常用的cron表达式示例：
- 每小时同步：`0 * * * *`
- 每天凌晨2点同步：`0 2 * * *`
- 每周一早上8点同步：`0 8 * * 1`

修改`.env`文件中的`SYNC_INTERVAL`可以自定义同步时间间隔。