# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : dependencies.py
@DateTime: 2025/6/7

Base 模块依赖注入工厂。

提供基础服务（审计日志等）CRUD 服务的依赖注入工厂函数。

使用方式:
    from fastapi import Depends
    from applications.base.dependencies import get_audit_crud
    
    @router.get("/list")
    async def list_audit(crud: AuditCrud = Depends(get_audit_crud)):
        return await crud.list_audit()
"""
from applications.base.services.audit_crud import AuditCrud


async def get_audit_crud() -> AuditCrud:
    """获取审计日志 CRUD 服务实例"""
    return AuditCrud()
