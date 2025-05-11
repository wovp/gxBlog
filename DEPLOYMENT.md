# gxBlog 项目部署指南

本文档提供了使用 Docker 和 Docker Compose 在云服务器上部署 gxBlog 项目的详细步骤。

## 前提条件

- 一台运行 Linux 的云服务器（推荐 Ubuntu 20.04 LTS 或更高版本）
- 已安装 Docker（版本 20.10 或更高）
- 已安装 Docker Compose（版本 2.0 或更高）
- 服务器开放了 80 端口（前端）和 8000 端口（后端，可选）

## 部署步骤

### 1. 准备工作

1. 将项目代码上传到服务器：

   ```bash
   # 在本地执行
   scp -r /path/to/gxBlog user@your-server-ip:/path/to/deploy
   ```

   或者使用 Git 克隆项目：

   ```bash
   # 在服务器上执行
   git clone https://github.com/your-username/gxBlog.git
   cd gxBlog
   ```

2. 确保后端环境变量配置正确：

   ```bash
   # 在服务器上执行
   cd /path/to/gxBlog/backend
   cp .env.example .env
   # 编辑 .env 文件，填入正确的配置
   nano .env
   ```

### 2. 修改配置（如需要）

1. 检查并修改 `docker-compose.yml` 文件中的配置：

   ```bash
   nano docker-compose.yml
   ```

2. 检查并修改前端 Nginx 配置：

   ```bash
   nano gxBlog/nginx.conf
   ```

### 3. 构建和启动容器

1. 在项目根目录下执行：

   ```bash
   docker-compose up -d --build
   ```

   这将构建镜像并在后台启动容器。

2. 检查容器是否正常运行：

   ```bash
   docker-compose ps
   ```

### 4. 访问应用

- 前端：http://your-server-ip
- 后端 API：http://your-server-ip/api

### 5. 查看日志

```bash
# 查看所有服务的日志
docker-compose logs

# 查看特定服务的日志
docker-compose logs backend
docker-compose logs frontend

# 实时查看日志
docker-compose logs -f
```

### 6. 停止和重启服务

```bash
# 停止所有服务
docker-compose down

# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart backend
```

## 注意事项

1. **数据持久化**：当前配置没有为数据库设置持久化卷。如果您使用外部数据库，请确保在 `.env` 文件中正确配置数据库连接信息。

2. **安全性**：
   - 生产环境中，应该限制 CORS 设置，只允许特定域名访问 API
   - 考虑使用 HTTPS，可以配合 Nginx 和 Let's Encrypt 实现
   - 不要在代码仓库中存储敏感信息，使用环境变量或 Docker secrets

3. **性能优化**：
   - 考虑使用 Nginx 缓存静态资源
   - 对于高流量网站，可以考虑使用负载均衡

## 故障排除

1. 如果容器无法启动，检查日志：

   ```bash
   docker-compose logs
   ```

2. 检查网络连接：

   ```bash
   docker network ls
   docker network inspect gxblog-network
   ```

3. 检查容器状态：

   ```bash
   docker ps -a
   ```

## 更新应用

当有新版本时，执行以下步骤更新应用：

```bash
# 拉取最新代码
git pull

# 重新构建并启动容器
docker-compose up -d --build
```

---

如有任何问题，请联系项目维护者或提交 Issue。