# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : example_view.py
@DateTime: 2025/6/7
"""
from decimal import Decimal

from fastapi import APIRouter, Body, Query, Depends
from tortoise.expressions import Q

from applications.example.dependencies import (
    get_category_crud,
    get_product_crud,
    get_example_services,
    ExampleServices,
)
from applications.example.schemas.example_schema import (
    CategoryCreate,
    CategoryUpdate,
    ProductCreate,
    ProductUpdate,
    BatchCreateProducts,
    BatchUpdateProducts,
    TransferStock,
)
from applications.example.services.example_crud import CategoryCrud, ProductCrud
from configure import LOGGER
from core.responses import SuccessResponse, FailureResponse

example_category = APIRouter()
example_product = APIRouter()


# ==================== 分类接口 ====================

@example_category.post("/category/create", summary="创建分类")
async def create_category(
        category_in: CategoryCreate = Body(),
        category_crud: CategoryCrud = Depends(get_category_crud),
):
    try:
        instance = await category_crud.create(category_in)
        data = await instance.to_dict()
        return SuccessResponse(data=data)
    except Exception as e:
        LOGGER.error(f"创建分类失败: {e}")
        return FailureResponse(message=f"创建失败: {e}")


@example_category.get("/category/list", summary="查询分类列表")
async def list_category(
        page: int = Query(default=1, ge=1, description="页码"),
        page_size: int = Query(default=10, ge=10, description="每页数量"),
        name: str = Query(default=None, description="分类名称"),
        state: int = Query(default=None, description="状态"),
        category_crud: CategoryCrud = Depends(get_category_crud),
):
    q = Q()
    if name:
        q &= Q(name__contains=name)
    if state is not None:
        q &= Q(state=state)
    else:
        q &= Q(state=0)

    total, items = await category_crud.list(page=page, page_size=page_size, search=q)
    data = [await item.to_dict() for item in items]
    return SuccessResponse(data=data, total=total)


@example_category.get("/category/get", summary="查询分类详情")
async def get_category(
        category_id: int = Query(..., description="分类ID"),
        category_crud: CategoryCrud = Depends(get_category_crud),
):
    instance = await category_crud.get_or_none(id=category_id)
    if not instance:
        return FailureResponse(message="分类不存在")
    data = await instance.to_dict()
    return SuccessResponse(data=data)


@example_category.post("/category/update", summary="更新分类")
async def update_category(
        category_in: CategoryUpdate = Body(),
        category_crud: CategoryCrud = Depends(get_category_crud),
):
    try:
        instance = await category_crud.update(
            id=category_in.category_id,
            obj_in=category_in
        )
        data = await instance.to_dict()
        return SuccessResponse(data=data)
    except Exception as e:
        LOGGER.error(f"更新分类失败: {e}")
        return FailureResponse(message=f"更新失败: {e}")


@example_category.delete("/category/delete", summary="删除分类")
async def delete_category(
        category_id: int = Query(..., description="分类ID"),
        category_crud: CategoryCrud = Depends(get_category_crud),
):
    try:
        instance = await category_crud.soft_delete(id=category_id)
        data = await instance.to_dict()
        return SuccessResponse(data=data)
    except Exception as e:
        LOGGER.error(f"删除分类失败: {e}")
        return FailureResponse(message=f"删除失败: {e}")


# ==================== 商品接口 ====================

@example_product.post("/product/create", summary="创建商品")
async def create_product(
        product_in: ProductCreate = Body(),
        product_crud: ProductCrud = Depends(get_product_crud),
):
    try:
        instance = await product_crud.create(product_in)
        data = await instance.to_dict()
        return SuccessResponse(data=data)
    except Exception as e:
        LOGGER.error(f"创建商品失败: {e}")
        return FailureResponse(message=f"创建失败: {e}")


@example_product.post("/product/batch_create", summary="批量创建商品")
async def batch_create_products(
        batch_in: BatchCreateProducts = Body(),
        product_crud: ProductCrud = Depends(get_product_crud),
):
    try:
        instances = await product_crud.batch_create(batch_in.products)
        data = [await item.to_dict() for item in instances]
        return SuccessResponse(data=data, total=len(data))
    except Exception as e:
        LOGGER.error(f"批量创建商品失败: {e}")
        return FailureResponse(message=f"批量创建失败: {e}")


@example_product.get("/product/list", summary="查询商品列表")
async def list_product(
        page: int = Query(default=1, ge=1, description="页码"),
        page_size: int = Query(default=10, ge=10, description="每页数量"),
        name: str = Query(default=None, description="商品名称"),
        category_id: int = Query(default=None, description="分类ID"),
        min_price: Decimal = Query(default=None, description="最低价格"),
        max_price: Decimal = Query(default=None, description="最高价格"),
        product_crud: ProductCrud = Depends(get_product_crud),
):
    q = Q()
    if name:
        q &= Q(name__contains=name)
    if category_id:
        q &= Q(category_id=category_id)
    if min_price is not None:
        q &= Q(price__gte=min_price)
    if max_price is not None:
        q &= Q(price__lte=max_price)
    q &= Q(state=0)

    total, items = await product_crud.list(page=page, page_size=page_size, search=q)
    data = [await item.to_dict() for item in items]
    return SuccessResponse(data=data, total=total)


@example_product.get("/product/query", summary="使用查询构建器查询商品")
async def query_products(
        category_id: int = Query(default=None, description="分类ID"),
        is_featured: bool = Query(default=None, description="是否推荐"),
        page: int = Query(default=1, ge=1, description="页码"),
        page_size: int = Query(default=10, ge=10, description="每页数量"),
        product_crud: ProductCrud = Depends(get_product_crud),
):
    """测试 QueryBuilder 功能"""
    try:
        builder = product_crud.query().filter(state=0)

        if category_id:
            builder = builder.filter(category_id=category_id)
        if is_featured is not None:
            builder = builder.filter(is_featured=is_featured)

        total, items = await builder.order_by("-created_time").paginate(page=page, page_size=page_size)
        data = [await item.to_dict() for item in items]
        return SuccessResponse(data=data, total=total)
    except Exception as e:
        LOGGER.error(f"查询商品失败: {e}")
        return FailureResponse(message=f"查询失败: {e}")


@example_product.get("/product/get", summary="查询商品详情")
async def get_product(
        product_id: int = Query(..., description="商品ID"),
        product_crud: ProductCrud = Depends(get_product_crud),
):
    instance = await product_crud.get_or_none(id=product_id)
    if not instance:
        return FailureResponse(message="商品不存在")
    data = await instance.to_dict()
    return SuccessResponse(data=data)


@example_product.post("/product/update", summary="更新商品")
async def update_product(
        product_in: ProductUpdate = Body(),
        product_crud: ProductCrud = Depends(get_product_crud),
):
    try:
        instance = await product_crud.update(
            id=product_in.product_id,
            obj_in=product_in
        )
        data = await instance.to_dict()
        return SuccessResponse(data=data)
    except Exception as e:
        LOGGER.error(f"更新商品失败: {e}")
        return FailureResponse(message=f"更新失败: {e}")


@example_product.post("/product/batch_update", summary="批量更新商品")
async def batch_update_products(
        batch_in: BatchUpdateProducts = Body(),
        product_crud: ProductCrud = Depends(get_product_crud),
):
    try:
        count = await product_crud.batch_update(batch_in.updates, strict=False)
        return SuccessResponse(data={"updated_count": count})
    except Exception as e:
        LOGGER.error(f"批量更新商品失败: {e}")
        return FailureResponse(message=f"批量更新失败: {e}")


@example_product.delete("/product/delete", summary="删除商品")
async def delete_product(
        product_id: int = Query(..., description="商品ID"),
        product_crud: ProductCrud = Depends(get_product_crud),
):
    try:
        instance = await product_crud.soft_delete(id=product_id)
        data = await instance.to_dict()
        return SuccessResponse(data=data)
    except Exception as e:
        LOGGER.error(f"删除商品失败: {e}")
        return FailureResponse(message=f"删除失败: {e}")


@example_product.post("/product/transfer_stock", summary="库存转移")
async def transfer_stock(
        transfer_in: TransferStock = Body(),
        product_crud: ProductCrud = Depends(get_product_crud),
):
    """测试事务装饰器"""
    try:
        result = await product_crud.transfer_stock(
            from_product_id=transfer_in.from_product_id,
            to_product_id=transfer_in.to_product_id,
            quantity=transfer_in.quantity
        )
        return SuccessResponse(data=result)
    except Exception as e:
        LOGGER.error(f"库存转移失败: {e}")
        return FailureResponse(message=f"库存转移失败: {e}")


@example_product.get("/product/statistics", summary="商品统计")
async def product_statistics(
        product_crud: ProductCrud = Depends(get_product_crud),
):
    """测试聚合统计功能"""
    try:
        stats = await product_crud.get_product_statistics()
        return SuccessResponse(data=stats)
    except Exception as e:
        LOGGER.error(f"获取统计失败: {e}")
        return FailureResponse(message=f"获取统计失败: {e}")


@example_product.get("/product/category_stats", summary="分类统计")
async def category_statistics(
        product_crud: ProductCrud = Depends(get_product_crud),
):
    """测试分组统计功能"""
    try:
        results = await product_crud.get_category_group_stats()
        return SuccessResponse(data=results)
    except Exception as e:
        LOGGER.error(f"获取分类统计失败: {e}")
        return FailureResponse(message=f"获取分类统计失败: {e}")


@example_product.get("/product/exists", summary="检查商品是否存在")
async def check_product_exists(
        code: str = Query(..., description="商品编码"),
        product_crud: ProductCrud = Depends(get_product_crud),
):
    """测试 exists 方法"""
    exists = await product_crud.exists(code=code)
    return SuccessResponse(data={"exists": exists})


# ==================== 组合依赖示例：需要同时使用多个 CRUD 的接口 ====================

@example_product.get("/product/with_category", summary="查询商品及分类信息")
async def get_product_with_category(
        product_id: int = Query(..., description="商品ID"),
        services: ExampleServices = Depends(get_example_services),
):
    """
    使用组合依赖同时获取商品和分类信息。
    
    展示如何在单个接口中使用多个 CRUD 实例。
    """
    try:
        product = await services.product.get_or_none(id=product_id)
        if not product:
            return FailureResponse(message="商品不存在")

        product_data = await product.to_dict()

        # 补充分类信息
        if product.category_id:
            category = await services.category.get_or_none(id=product.category_id)
            if category:
                product_data["category"] = await category.to_dict()

        return SuccessResponse(data=product_data)
    except Exception as e:
        LOGGER.error(f"查询商品详情失败: {e}")
        return FailureResponse(message=f"查询失败: {e}")
