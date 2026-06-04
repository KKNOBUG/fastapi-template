# 基于 FastAPI 和 Tortoise ORM 的现代 Web 应用程序模板

## 项目概述

本文档全面介绍了FastAPI模板存储库，总结了其用途、架构设计和主要组件。此模板是使用FastAPI和Tortoise ORM构建现代、高性能Web应用程序的基础。

## 目的和范围

本项目是一个现代的 Web 应用程序开发模板，旨在为开发者提供一个高效、便捷且可扩展的开发基础。
它基于 FastAPI 和 Tortoise ORM 这两个强大的 Python 库构建，结合了 FastAPI 的高性能、简洁性与 Tortoise ORM
的易用性和灵活性，能够帮助开发者快速搭建出高质量的 Web 应用。

该模板满足了几个关键需求：

- 结构化项目组织
- 简化的应用程序初始化
- 数据库与异步ORM集成
- 全面的配置管理
- 标准化的错误处理和记录
- 通用操作的公用事业系统

## 核心技术选择

该模板集成了几种关键技术，以提供完整的开发环境：


| 技术           | 目的               | 版本      |
|--------------|------------------|---------|
| FastAPI      | 构建API的网络框架       | 0.115.6 |
| Tortoise ORM | 用于数据库操作的非同步ORM   | 0.23.0  |
| Pydantic     | 数据验证和配置          | 2.10.6  |
| Uvicorn      | 用于运行应用程序的ASGI服务器 | 0.33.0  |
| Loguru       | 增强的日志记录功能        | 0.6.0   |

## 项目结构

```text

fastapi-template
├── applications
│   ├── base
│   │   ├── models
│   │   ├── schemas
│   │   ├── services
│   │   ├── tasks
│   │   └── views
│   ├── ...
│   └── ...
├── common
├── configure
├── core
├── enums
├── output
├── services
├── static
│   ├── swagger-ui
│   │   ├── swagger-ui.css
│   │   ├── swagger-ui-bundle.js
│   │   └── favicon-32x32.png
├── .env
├── .gitignore
├── README.md
└── main.py

```