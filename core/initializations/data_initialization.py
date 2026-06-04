# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : KeenRunner Template
@Module  : data_initialization.py
@DateTime: 2025/2/19 22:12
"""
from fastapi import FastAPI

from applications.user.schemas.user_schema import UserCreate
from applications.user.services.user_crud import USER_CRUD


async def init_database_user():
    user = await USER_CRUD.model.exists()
    if not user:
        await USER_CRUD.create_user(
            UserCreate(
                username="admin",
                password="123456",
                alias="系统管理员",
                email="admin@test.com",
                phone="18888888888",
                avatar="/static/avatar/default/20250101010101.png",
                state=0,
                is_active=True,
                is_superuser=True,
            )
        )


async def init_database_table(app: FastAPI):
    await init_database_user()
