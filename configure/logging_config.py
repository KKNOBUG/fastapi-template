# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : logging_config.py
@DateTime: 2025/1/16 15:33
"""
import os
import sys
import logging
import logging.config

from loguru import logger

from configure.project_config import PROJECT_CONFIG


def loguru_logging() -> logger:
    # 移除默认配置
    logger.remove()

    # 自定义日志格式
    format_str = (
        # 时间信息
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        # 日志级别，居中对齐
        "<level>{level: ^8}</level> | "
        # 进程和线程信息
        "process [<cyan>{process}</cyan>]:<cyan>{thread}</cyan> | "
        # 文件、函数和行号
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> -> "
        # 日志消息
        "<level>{message}</level>"
    )

    # 添加文件处理器（异常）
    logger.add(
        os.path.join(PROJECT_CONFIG.OUTPUT_LOGS_DIR, "{time:YYYYMMDD}_ERROR_执行日志.log"),
        format=format_str,
        level="ERROR",
        encoding='utf-8',
        rotation=PROJECT_CONFIG.LOGGER_ROTATION,
        retention=PROJECT_CONFIG.LOGGER_RETENTION,
        compression=PROJECT_CONFIG.LOGGER_COMPRESSION,
        enqueue=True,  # 是否启用异步安全队列写入
        backtrace=True,  # 是否启用完整的异常回溯
    )

    # 添加文件处理器（信息）
    logger.add(
        os.path.join(PROJECT_CONFIG.OUTPUT_LOGS_DIR, "{time:YYYYMMDD}_INFO_执行日志.log"),
        format=format_str,
        level="INFO",
        encoding='utf-8',
        rotation=PROJECT_CONFIG.LOGGER_ROTATION,
        retention=PROJECT_CONFIG.LOGGER_RETENTION,
        compression=PROJECT_CONFIG.LOGGER_COMPRESSION,
        enqueue=True,  # 是否启用异步安全队列写入
        backtrace=True,  # 是否启用完整的异常回溯
        filter=lambda record: record["level"].no < logger.level("ERROR").no  # 过滤掉 ERROR 及以上级别的日志
    )

    # 控制台输出
    if PROJECT_CONFIG.SERVER_DEBUG:
        logger.add(
            sys.stdout,
            format=format_str,
            enqueue=True,  # 是否启用异步安全队列写入
            backtrace=True,  # 是否启用完整的异常回溯
            colorize=True,  # 是否启用控制台输出彩色
            diagnose=True,  # 是否启用变量值诊断信息
        )

    # 配置标准库日志
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    _logger = logging.getLogger("uvicorn.error")
    _logger.setLevel("INFO")

    return logger


class InterceptHandler(logging.Handler):
    """
    日志拦截处理器：将所有 Python 标准日志重定向到 Loguru

    工作原理：
    1. 继承自 logging.Handler
    2. 重写 emit 方法处理日志记录
    3. 将标准库日志转换为 Loguru 格式
    """
    # 排除logger name
    EXCLUDED_LOGGERS: set = {
        "aiomysql",
        "asyncio",
        "tortoise",
        "tortoise.db_client",
        "uvicorn.asgi",
        "uvicorn.middleware.*",
        "python_multipart.*",
    }

    def is_excluded(self, name: str) -> bool:
        for excluded in self.EXCLUDED_LOGGERS:
            if excluded.endswith(".*"):
                if name.startswith(excluded[:-1]):
                    return True
            elif name == excluded:
                return True
        return False

    def emit(self, record: logging.LogRecord) -> None:
        if self.is_excluded(record.name):
            return

        # 获取发出日志的调用者
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # 使用 Loguru 记录日志
        logger.opt(depth=depth, exception=record.exc_info).log(
            "INFO",
            record.getMessage()
        )
