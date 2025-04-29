# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : app_initialization.py
@DateTime: 2025/1/17 21:55
"""
import os
import sys
import shutil
from datetime import datetime
from typing import Dict, Any

from loguru import logger
from aerich import Command
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

from configure.project_config import PROJECT_CONFIG
from configure.logging_config import loguru_logging
from core.exceptions.http_exceptions import (
    request_validation_exception_handler,
    response_validation_exception_handler,
    http_exception_handler,
    null_point_exception_handler,
    app_exception_handler
)
from core.middlewares.app_middleware import logging_middleware


def register_logging() -> logger:
    return loguru_logging()


async def register_database(app: FastAPI) -> None:
    config: Dict[str, Any] = {
        "connections": PROJECT_CONFIG.DATABASE_CONNECTIONS,
        "apps": {
            "models": {
                "models": PROJECT_CONFIG.APPLICATIONS_MODELS,
                "default_connection": "default"
            }
        },
        "use_tz": False,
        "timezone": "Asia/Shanghai",
    }
    register_tortoise(
        app=app,
        config=config,
        generate_schemas=False,
        add_exception_handlers=PROJECT_CONFIG.SERVER_DEBUG,
    )

    # 确保迁移目录存在
    if not os.path.exists(PROJECT_CONFIG.MIGRATION_DIR):
        os.makedirs(PROJECT_CONFIG.MIGRATION_DIR)

    # 初始化Aerich命令
    command = Command(
        app='models',
        tortoise_config=config,
        location=PROJECT_CONFIG.MIGRATION_DIR,
    )

    # 初始化数据库和迁移
    try:
        # 当 safe 设置为 True 时，如果数据库中已经存在 Aerich 所需的迁移表（通常是 aerich 表），init_db 方法不会尝试去重新创建这些表，避免因为表已存在而抛出错误。
        # 当 safe 设置为 False 时，如果数据库中已经存在 Aerich 所需的迁移表，init_db 方法会尝试重新创建这些表，这可能会导致现有表被删除并重新创建，从而丢失表中的数据。
        await command.init_db(safe=True)
    except FileExistsError:
        pass

    await command.init()

    # 生成迁移文件
    try:
        await command.migrate(name=f"auto_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    except AttributeError as e:
        print("无法从数据库中检索模型历史记录，模型历史记录将从头创建")
        shutil.rmtree(PROJECT_CONFIG.MIGRATION_DIR)
        await command.init_db(safe=True)

    # 应用迁移
    await command.upgrade(run_in_transaction=True)


# 注册异常处理器
def register_exceptions(app: FastAPI) -> None:
    # 当 FastAPI 在解析和验证请求数据时发现问题，会触发 RequestValidationError 异常
    app.add_exception_handler(
        exc_class_or_status_code=RequestValidationError,
        handler=request_validation_exception_handler
    )
    # 当 FastAPI 在解析和验证响应数据时发现问题，会触发 ResponseValidationError 异常
    app.add_exception_handler(
        exc_class_or_status_code=ResponseValidationError,
        handler=response_validation_exception_handler
    )
    # 当发生 HTTP 相关的异常时，如 403 禁止访问、404 未找到等，会触发 HTTPException 异常
    app.add_exception_handler(
        exc_class_or_status_code=HTTPException,
        handler=http_exception_handler
    )
    # 当使用 Tortoise ORM 进行数据库查询时，如果查询结果为空，会触发 DoesNotExist 异常
    app.add_exception_handler(
        exc_class_or_status_code=DoesNotExist,
        handler=null_point_exception_handler
    )
    # 当发生未被其他特定异常处理器处理的异常时，会触发此函数
    app.add_exception_handler(
        exc_class_or_status_code=Exception,
        handler=app_exception_handler
    )


def register_middlewares(app: FastAPI):
    # 注册 CORS 中间件，CORS（跨域资源共享）中间件用于处理跨域请求，允许不同域名的客户端访问服务器资源
    app.add_middleware(
        CORSMiddleware,
        allow_origins=PROJECT_CONFIG.CORS_ORIGINS,
        allow_credentials=PROJECT_CONFIG.CORS_ALLOW_CREDENTIALS,
        allow_methods=PROJECT_CONFIG.CORS_ALLOW_METHODS,
        allow_headers=PROJECT_CONFIG.CORS_ALLOW_HEADERS,
        expose_headers=PROJECT_CONFIG.CORS_EXPOSE_METHODS,
        max_age=PROJECT_CONFIG.CORS_MAX_AGE,
    )
    # 注册 HTTP 请求中间件
    app.middleware('http')(logging_middleware)


def register_routers(app: FastAPI) -> None:
    # 挂载静态文件
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.openapi_version = PROJECT_CONFIG.APP_OPENAPI_VERSION
    static_modules = sys.modules["fastapi.openapi.docs"].get_swagger_ui_html.__kwdefaults__
    static_modules["swagger_js_url"] = PROJECT_CONFIG.APP_OPENAPI_JS_URL
    static_modules["swagger_css_url"] = PROJECT_CONFIG.APP_OPENAPI_CSS_URL
    static_modules["swagger_favicon_url"] = PROJECT_CONFIG.APP_OPENAPI_FAVICON_URL

    # 导入路由蓝图

    # 挂在路由蓝图
