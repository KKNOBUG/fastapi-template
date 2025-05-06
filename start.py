# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : start
@DateTime: 2025/4/28 18:06
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute
from tortoise import Tortoise

from core import GLOBAL_CONFIG, PROJECT_CONFIG, LOGGER
from core.initializations.app_initialization import (
    register_logging,
    register_exceptions,
    register_middlewares,
    register_routers,
)

from core.responses.http_response import SuccessResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    for route in app.routes:
        if isinstance(route, APIRoute):
            GLOBAL_CONFIG.ROUTER_SUMMARY[route.path] = route.summary
            GLOBAL_CONFIG.ROUTER_TAGS[route.path] = route.tags

    yield

    await Tortoise.close_connections()


app = FastAPI(
    title=PROJECT_CONFIG.APP_TITLE,
    description=PROJECT_CONFIG.APP_DESCRIPTION,
    version=PROJECT_CONFIG.APP_VERSION,
    docs_url=PROJECT_CONFIG.APP_DOCS_URL,
    redoc_url=PROJECT_CONFIG.APP_REDOC_URL,
    openapi_url=PROJECT_CONFIG.APP_OPENAPI_URL,
    debug=PROJECT_CONFIG.SERVER_DEBUG,
    lifespan=lifespan,
)

register_logging()
register_exceptions(app)
register_middlewares(app)
register_routers(app)


@app.get("/")
async def root():
    return SuccessResponse(message="FastAPI Started Successfully!")


if __name__ == '__main__':
    import uvicorn

    banner: str = f"""            
    ▄▄▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    █░░░░░░░░░░░█  █░░░░░░░░░░░░█  █░░░░░░░░░░░░█  █░░░░░░░░░░░░█  █░░░░░░░░░░░░█  █░░░░░░░░░░░░█  █░░░░░░░░░░░░█
    █░█▀▀▀▀▀▀▀▀▀▀  █░█▀▀▀▀▀▀▀▀█░█  █░█▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀█░█▀▀▀▀▀  █░█▀▀▀▀▀▀▀▀█░█  █░█▀▀▀▀▀▀▀▀█░█  ▀▀▀▀▀█░░█▀▀▀▀▀ 
    █░█▄▄▄▄▄▄▄▄▄▄  █░█▄▄▄▄▄▄▄▄█░█  █░█▄▄▄▄▄▄▄▄▄▄▄        █░█       █░█▄▄▄▄▄▄▄▄█░█  █░█▄▄▄▄▄▄▄▄█░█       █░░█     
    █░░░░░░░░░░░█  █░░░░░░░░░░░░█  █░░░░░░░░░░░░█        █░█       █░░░░░░░░░░░░█  █░░░░░░░░░░░░█       █░░█     
    █░█▀▀▀▀▀▀▀▀▀▀  █░█▀▀▀▀▀▀▀▀█░█  ▀▀▀▀▀▀▀▀▀▀▀█░█        █░█       █░█▀▀▀▀▀▀▀▀█░█  █░█▀▀▀▀▀▀▀▀▀▀        █░░█     
    █░█            █░█        █░█             █░█        █░█       █░█        █░█  █░█                  █░░█    
    █░█            █░█        █░█  ▄▄▄▄▄▄▄▄▄▄▄█░█        █░█       █░█        █░█  █░█             ▄▄▄▄▄█░░█▄▄▄▄▄ 
    █░█            █░█        █░█  █░░░░░░░░░░░░█        █░█       █░█        █░█  █░█             █░░░░░░░░░░░░█
    ▀▀▀            ▀▀▀        ▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀        ▀▀▀       ▀▀▀        ▀▀▀  ▀▀▀             ▀▀▀▀▀▀▀▀▀▀▀▀▀▀

    环境名称：{PROJECT_CONFIG.ENV_NAME}
    服务主机：{PROJECT_CONFIG.SERVER_HOST}
    服务端口：{PROJECT_CONFIG.SERVER_PORT}
    """
    LOGGER.info(banner)
    uvicorn.run(
        app=PROJECT_CONFIG.SERVER_APP,
        host=PROJECT_CONFIG.SERVER_HOST,
        port=PROJECT_CONFIG.SERVER_PORT,
        reload=PROJECT_CONFIG.SERVER_DEBUG,
        reload_delay=PROJECT_CONFIG.SERVER_DELAY,
        log_config=None,
    )

    # 记录依赖：pip list --format=freeze > requirements.txt
