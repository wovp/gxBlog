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
- 文章详情、分类、标签
- 个人主页（homepage 子项目集成）
- 支持 Markdown 编辑与渲染
- 响应式设计，适配多端
- 后台 API 支持文章、用户等管理

## 环境依赖
- Node.js >= 16.x
- Python >= 3.8
- Docker & Docker Compose（可选）

## 安装与启动

详细的部署过程可以看：https://mp.weixin.qq.com/s/e0BzkEckKNxBFj3M_F1Bcw

如需更多帮助或有任何疑问，请联系项目维护者。
