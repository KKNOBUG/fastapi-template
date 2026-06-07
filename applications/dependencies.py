# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : dependencies.py
@DateTime: 2025/6/7

依赖注入工厂模块。

提供各模块 CRUD 服务的依赖注入工厂函数，用于替代全局 *_CRUD 实例。
使用 FastAPI 的 Depends 机制，确保每次请求创建新的 CRUD 实例，
避免异步生命周期和连接状态问题。

使用方式:
    from fastapi import Depends
    from applications.example.dependencies import get_product_crud
    
    @router.post("/create")
    async def create(data: ProductCreate, crud: ProductCrud = Depends(get_product_crud)):
        return await crud.create(data)
"""
from dataclasses import dataclass

from applications.base.services.audit_crud import AuditCrud
from applications.example.services.example_crud import CategoryCrud, ProductCrud
from applications.user.services.user_crud import UserCrud


@dataclass
class ExampleServices:
    """
    Example 模块服务组合。
    
    用于需要同时操作分类和商品的复杂业务场景。
    
    使用示例:
        @router.post("/order/create")
        async def create_order(
            data: OrderCreate,
            services: ExampleServices = Depends(get_example_services)
        ):
            category = await services.category.get_or_none(id=data.category_id)
            product = await services.product.create(data)
            ...
    """
    category: CategoryCrud
    product: ProductCrud


async def get_category_crud() -> CategoryCrud:
    """获取分类 CRUD 服务实例"""
    return CategoryCrud()


async def get_product_crud() -> ProductCrud:
    """获取商品 CRUD 服务实例"""
    return ProductCrud()


async def get_example_services() -> ExampleServices:
    """
    获取 Example 模块组合服务。
    
    同时提供分类和商品 CRUD 实例，适用于需要多模型联动的接口。
    """
    return ExampleServices(
        category=CategoryCrud(),
        product=ProductCrud(),
    )


# ==================== User 模块依赖（独立依赖） ====================

async def get_user_crud() -> UserCrud:
    """获取用户 CRUD 服务实例"""
    return UserCrud()


# ==================== Base 模块依赖（独立依赖） ====================

async def get_audit_crud() -> AuditCrud:
    """获取审计日志 CRUD 服务实例"""
    return AuditCrud()
