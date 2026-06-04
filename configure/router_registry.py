# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : KeenRunner Template
@Module  : router_registry.py
@DateTime: 2026/5/27
"""
from typing import Any, Dict

# 应用启动后由 lifespan 填充，供日志中间件读取
ROUTER_SUMMARY: Dict[str, Any] = {}
ROUTER_TAGS: Dict[str, Any] = {}
