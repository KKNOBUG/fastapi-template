# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : KeenRunner Template
@Module  : __init__.py
@DateTime: 2025/1/12 19:42
"""
from fastapi import APIRouter

from .auth_view import auth_public, auth_secure

base_public = APIRouter()
base_secure = APIRouter()

base_public.include_router(auth_public, prefix="/auth")
base_secure.include_router(auth_secure, prefix="/auth")
