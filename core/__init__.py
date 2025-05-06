# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : __init__.py
@DateTime: 2025/4/28 18:05
"""

from configure.global_config import GLOBAL_CONFIG
from configure.project_config import PROJECT_CONFIG
from configure.logging_config import logger as LOGGER

__all__ = (
    GLOBAL_CONFIG,
    PROJECT_CONFIG,
    LOGGER,

)
