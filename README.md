# 基于 FastAPI 和 Tortoise ORM 的现代 Web 应用程序模板

## 项目概述
本项目是一个现代的 Web 应用程序开发模板，旨在为开发者提供一个高效、便捷且可扩展的开发基础。它基于 FastAPI 和 Tortoise ORM 这两个强大的 Python 库构建，结合了 FastAPI 的高性能、简洁性与 Tortoise ORM 的易用性和灵活性，能够帮助开发者快速搭建出高质量的 Web 应用。

## 核心技术选择
### FastAPI
FastAPI 是一个基于 Python 的现代、快速（高性能）的 Web 框架，它利用 Python 的类型提示来提高代码的可读性和可维护性，同时具备自动生成交互式 API 文档的能力。FastAPI 基于 Starlette 和 Pydantic 构建，支持异步编程，能够处理高并发请求，为应用提供了出色的性能表现。

### Tortoise ORM
Tortoise ORM 是一个专为 Python 设计的异步 ORM（对象关系映射）库，它与 FastAPI 的异步特性完美结合。Tortoise ORM 提供了简单而直观的 API，使得开发者可以方便地进行数据库操作，如创建、读取、更新和删除数据。它支持多种数据库，包括 SQLite、MySQL、PostgreSQL 等，为项目的数据库选择提供了灵活性。


## 项目结构
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