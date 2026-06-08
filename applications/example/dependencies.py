# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : dependencies.py
@DateTime: 2025/6/7

Example 模块依赖注入工厂。

提供示例模块（分类、商品）CRUD 服务的依赖注入工厂函数。
支持独立依赖和组合依赖两种使用方式。

使用方式:
    # 独立依赖
    from applications.example.dependencies import get_product_crud
    
    @router.post("/create")
    async def create(data: ProductCreate, crud: ProductCrud = Depends(get_product_crud)):
        return await crud.create(data)
    
    # 组合依赖（多模型联动）
    from applications.example.dependencies import get_example_services, ExampleServices
    
    @router.post("/order")
    async def create_order(data: OrderCreate, services: ExampleServices = Depends(get_example_services)):
        product = await services.product.get_or_none(id=data.product_id)
        category = await services.category.get_or_none(id=product.category_id)
        ...
"""
from dataclasses import dataclass

from applications.example.services.example_crud import CategoryCrud, ProductCrud


@dataclass
class ExampleServices:
    """
    Example 模块服务组合。
    
    用于需要同时操作分类和商品的复杂业务场景。
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
