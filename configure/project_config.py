# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : project_config.py
@DateTime: 2025/1/15 16:08
"""
import os.path
import platform
from typing import List, Dict, Any

from pydantic_settings import BaseSettings

from common.file_utils import FileUtils
from common.shell_utils import ShellUtils


class ProjectConfig(BaseSettings):
    # 项目描述
    APP_VERSION: str = "0.1.1"
    APP_TITLE: str = "Fastapi Application"
    APP_DESCRIPTION: str = "Fastapi Application"
    APP_DOCS_URL: str = "/docs"
    APP_REDOC_URL: str = "/redoc"
    APP_OPENAPI_URL: str = "/openapi_url"
    APP_OPENAPI_JS_URL: str = "/static/swagger-ui/swagger-ui-bundle.js"
    APP_OPENAPI_CSS_URL: str = "/static/swagger-ui/swagger-ui.css"
    APP_OPENAPI_FAVICON_URL: str = "/static/swagger-ui/favicon-32x32.png"
    APP_OPENAPI_VERSION: str = "3.0.2"

    # 调试配置
    SERVER_APP: str = "start:app"
    SERVER_HOST: str = ShellUtils.acquire_localhost()
    SERVER_SYSTEM: str = platform.system()
    SERVER_PORT: int = 8518
    SERVER_DEBUG: bool = SERVER_SYSTEM != "Linux"  # Windows | Linux | Darwin
    SERVER_DELAY: int = 5

    # 安全认证配置
    AUTH_SECRET_KEY: str = "3488a63e1765035d386f05409663f55c83bfae3b3c61a932744b20ad14244dcf"  # openssl rand -hex 32
    AUTH_JWT_ALGORITHM: str = "HS256"
    AUTH_JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 day

    # 日志相关参数配置
    # 文件大小轮转
    # 日期轮转："1 day"、"1 week"、"1 month"
    # 时间轮转："HH:MM:SS"、"00:00"、"00:00:00"
    LOGGER_ROTATION: str = '00:00:00'
    # 保留30天
    LOGGER_RETENTION: str = '30 days'
    # 压缩格式
    LOGGER_COMPRESSION: str = "zip"

    # 项目路径相关配置
    PROJECT_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    APPLICATIONS_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, "applications"))
    COMMON_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, "common"))
    CONFIGURE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, "configure"))
    CORE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, "core"))
    DECORATORS_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, "decorators"))
    ENUMS_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, "enums"))
    OUTPUT_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, "output"))
    OUTPUT_DOCS_DIR: str = os.path.abspath(os.path.join(OUTPUT_DIR, "docs"))
    OUTPUT_DOWNLOAD_DIR: str = os.path.abspath(os.path.join(OUTPUT_DIR, "download"))
    OUTPUT_LOGS_DIR: str = os.path.abspath(os.path.join(OUTPUT_DIR, "logs"))
    OUTPUT_UPLOAD_DIR: str = os.path.abspath(os.path.join(OUTPUT_DIR, "upload"))
    SERVICES_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, "services"))
    STATIC_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, "static"))
    STATIC_IMG_DIR: str = os.path.abspath(os.path.join(STATIC_DIR, "image"))
    MIGRATION_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, "migrations"))

    # # 允许访问的源（域名）列表
    CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:5000",
        "http://localhost:5173",
        "http://localhost:8000",
        "http://localhost:8515",
        "*",
    ]
    # 是否允许携带凭证（如 cookies）
    CORS_ALLOW_CREDENTIALS: bool = True
    # 允许的 HTTP 方法列表
    CORS_ALLOW_METHODS: List[str] = ["*"]
    # 允许的请求头列表
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    # 允许客户端访问的响应头列表
    CORS_EXPOSE_METHODS: List[str] = ["*"]
    # 预检请求的缓存时间（秒）
    CORS_MAX_AGE: int = 600

    # 文件上传设置
    UPLOAD_FILE_BASE_SIZE: int = 1024 * 1024  # 1MB
    UPLOAD_FILE_PEAK_SIZE: Dict[str, int] = {
        "tiny": UPLOAD_FILE_BASE_SIZE * 32,
        "micro": UPLOAD_FILE_BASE_SIZE * 64,
        "small": UPLOAD_FILE_BASE_SIZE * 128,
        "medium": UPLOAD_FILE_BASE_SIZE * 256,
        "large": UPLOAD_FILE_BASE_SIZE * 512,
        "huge": UPLOAD_FILE_BASE_SIZE * 1024,
    }
    UPLOAD_FILE_SUFFIX: List[str] = [
        'image/jepg',
        'image/png',
        'text/csv',
        'text/plain',
        'text/markdown',
        'application/pdf',
        'application/zip',
        'application/msword',  # doc
        'application/octet-stream',  # dat
        'application/vnd.ms-excel',  # xls
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # xlsx
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'  # docx
    ]

    # 应用注册
    APPLICATIONS_MODULE: str = "backend.applications"
    APPLICATIONS_INSTALLED: List[str] = FileUtils.get_all_dirs(
        abspath=APPLICATIONS_DIR,
        return_full_path=False,
        exclude_startswith="__",
        exclude_endswith="__",
    )

    @property
    def APPLICATIONS_MODELS(self) -> List[str]:
        models = [
            models
            for app in self.APPLICATIONS_INSTALLED
            for models in FileUtils.get_all_files(
                abspath=os.path.join(self.APPLICATIONS_DIR, app, "models"),
                return_full_path=False,
                return_precut_path=f"{self.APPLICATIONS_MODULE}.{app}.models.",
                endswith="model",
                exclude_startswith="__",
                exclude_endswith="__.py"
            )
        ]
        models.append("aerich.models")
        return models

    # 常用的用户代理字符串列表
    USER_AGENTS: List[str] = [
        # Chrome
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",

        # Firefox
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (X11; Linux i686; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:119.0) Gecko/20100101 Firefox/119.0",

        # Safari
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",

        # Edge
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",

        # Mobile
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    ]

    # 数据库配置
    # DATABASE_USERNAME: str = quote("username")
    # DATABASE_PASSWORD: str = quote("password")
    DATABASE_USERNAME: str = ""
    DATABASE_PASSWORD: str = ""
    DATABASE_HOST: str = ""
    DATABASE_PORT: str = "3306"
    DATABASE_NAME: str = "krun"
    DATABASE_URL: str = f"mysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}?charset=utf8mb4&time_zone=+08:00"
    DATABASE_CONNECTIONS: Dict[str, Any] = {
        "default": {
            "engine": "tortoise.backends.mysql",  # 使用mysql引擎
            "db_url": DATABASE_URL,
            "credentials": {
                "host": DATABASE_HOST,  # 数据库地址
                "port": DATABASE_PORT,  # 数据库端口
                "user": DATABASE_USERNAME,  # 数据库账户
                "password": DATABASE_PASSWORD,  # 数据库密码
                "database": DATABASE_NAME,  # 数据库名称
                "minsize": 10,  # 连接池最小连接数
                "maxsize": 40,  # 连接池最大连接数
                "charset": "utf8mb4",  # 数据库字符编码
                "echo": False,  # 数据库是否开启SQL语句回响
                "autocommit": True  # 数据库是否开启SQL语句自动提交
            }
        }
    }

    # Redis 配置
    REDIS_USERNAME: str = ""
    REDIS_PASSWORD: str = ""
    REDIS_HOST: str = ""
    REDIS_PORT: str = ""
    REDIS_URL: str = f"redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"


PROJECT_CONFIG = ProjectConfig()
