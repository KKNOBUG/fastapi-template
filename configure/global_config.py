# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : global_config.py
@DateTime: 2025/1/16 15:30
"""
from typing import Dict, Any

from pydantic_settings import BaseSettings


class GlobalConfig(BaseSettings):
    ROUTER_SUMMARY: Dict[str, Any] = {}
    ROUTER_TAGS: Dict[str, Any] = {}
    DATE_FORMAT: str = "%Y-%m-%d"
    TIME_FORMAT: str = "%H:%M:%S"
    DATETIME_FORMAT1: str = "%Y%m%d%H%M%S"
    DATETIME_FORMAT2: str = "%Y-%m-%d %H:%M:%S"


GLOBAL_CONFIG = GlobalConfig()
