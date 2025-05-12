# gxBlog 项目说明

## 项目简介

gxBlog 是一个基于 Vue 3、TypeScript 和 Vite 构建的现代化博客系统，支持前后端分离，包含前端页面与后端 API 服务。前端采用 Vue3 + Vite 技术栈，后端基于 Python FastAPI 实现，支持 Docker 一键部署。

## 目录结构

```
├── backend/           # 后端 FastAPI 服务
├── gxBlog/            # 前端 Vue3 项目
│   ├── public/        # 静态资源目录（含 homepage 子项目）
│   ├── src/           # 前端源码
│   ├── package.json   # 前端依赖配置
│   └── ...
├── docker-compose.yml # 一键部署配置
└── ...
```

## 主要功能
- 博客文章展示与管理
- 文章详情、分类、标签、搜索
- 个人主页（homepage 子项目集成）
- 支持 Markdown 编辑与渲染
- 响应式设计，适配多端
- 后台 API 支持文章、用户等管理

## 环境依赖
- Node.js >= 16.x
- Python >= 3.8
- Docker & Docker Compose（可选）

## 安装与启动

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd gxBlog
```

### 2. 安装前端依赖并启动
```bash
cd gxBlog
yarn install # 或 npm install
npm run dev
```

### 3. 启动后端服务
```bash
cd ../backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 4. Docker 一键部署（可选）
```bash
docker-compose up --build
```

## 打包与部署

前端打包：
```bash
cd gxBlog
npm run build
```
打包后静态文件位于 `gxBlog/dist`，可部署至任意静态服务器。

## 目录说明
- `gxBlog/public/homepage/`：个人主页子项目静态资源，已通过 `/homepage` 路由集成到主站。
- `backend/`：FastAPI 后端服务，包含 API、数据库模型、定时任务等。
- `docker-compose.yml`：支持前后端一键部署。

## 相关文档
- [Vue3 官方文档](https://vuejs.org/)
- [Vite 官方文档](https://vitejs.dev/)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)

---

如需更多帮助或有任何疑问，请联系项目维护者。
