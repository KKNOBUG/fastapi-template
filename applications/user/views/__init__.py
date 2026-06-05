# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : __init__.py
@DateTime: 2025/4/28 18:07
"""
from fastapi import APIRouter

from .user_view import user_public, user_secure

user_public_router = APIRouter()
user_secure_router = APIRouter()

user_public_router.include_router(user_public)
user_secure_router.include_router(user_secure)
