# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : init_data
@DateTime: 2026/6/7 12:39
"""
from applications.user.models.user_model import User


async def init_database_user():
    """初始化默认用户数据"""
    user = await User.exists()
    if not user:
        user_data = {
            "username": "admin",
            "password": "123456",
            "alias": "系统管理员",
            "email": "admin@test.com",
            "phone": "18888888888",
            "avatar": "/static/avatar/default/20250101010101.png",
            "is_active": True,
            "is_superuser": True,
        }
        await User.create(**user_data)
