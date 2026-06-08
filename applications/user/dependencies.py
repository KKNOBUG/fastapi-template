# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : dependencies.py
@DateTime: 2025/6/7

User 模块依赖注入工厂。

提供用户相关 CRUD 服务的依赖注入工厂函数。
使用 FastAPI 的 Depends 机制，确保每次请求创建新的 CRUD 实例。

使用方式:
    from fastapi import Depends
    from applications.user.dependencies import get_user_crud
    
    @router.post("/create")
    async def create(data: UserCreate, crud: UserCrud = Depends(get_user_crud)):
        return await crud.create(data)
"""
from applications.user.services.user_crud import UserCrud


async def get_user_crud() -> UserCrud:
    """获取用户 CRUD 服务实例"""
    return UserCrud()
