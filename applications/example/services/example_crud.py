# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : example_crud.py
@DateTime: 2025/6/7
"""
from typing import Optional, List, Dict, Any

from tortoise.expressions import Q, F
from tortoise.functions import Sum, Avg, Max, Min, Count

from applications.base.services.scaffold import ScaffoldCrud
from applications.example.models.example_model import Category, Product
from applications.example.schemas.example_schema import (
    CategoryCreate,
    CategoryUpdate,
    ProductCreate,
    ProductUpdate,
)
from configure import LOGGER


class CategoryCrud(ScaffoldCrud[Category, CategoryCreate, CategoryUpdate]):
    def __init__(self):
        super().__init__(model=Category)

    async def get_by_code(self, code: str) -> Optional[Category]:
        """根据编码获取分类"""
        return await self.model.filter(code=code).first()


class ProductCrud(ScaffoldCrud[Product, ProductCreate, ProductUpdate]):
    def __init__(self):
        super().__init__(model=Product)

    async def get_by_code(self, code: str) -> Optional[Product]:
        """根据编码获取商品"""
        return await self.model.filter(code=code).first()

    async def get_by_category(self, category_id: int, page: int = 1, page_size: int = 10):
        """获取分类下的商品"""
        q = Q(category_id=category_id, state=0)
        return await self.list(page=page, page_size=page_size, search=q)

    @ScaffoldCrud.transactional
    async def transfer_stock(
            self,
            from_product_id: int,
            to_product_id: int,
            quantity: int,
            _connection=None
    ) -> Dict[str, Any]:
        """
        库存转移（事务操作）
        
        验证事务装饰器是否正确传递 connection
        """
        # 检查转出商品库存
        from_product = await self.get_or_error(id=from_product_id)
        if from_product.stock < quantity:
            raise ValueError(f"库存不足，当前库存: {from_product.stock}")

        # 检查转入商品
        to_product = await self.get_or_error(id=to_product_id)

        # 执行库存转移
        if _connection:
            await self.model.filter(id=from_product_id).using_db(_connection).update(
                stock=F('stock') - quantity
            )
            await self.model.filter(id=to_product_id).using_db(_connection).update(
                stock=F('stock') + quantity
            )
        else:
            await self.model.filter(id=from_product_id).update(stock=F('stock') - quantity)
            await self.model.filter(id=to_product_id).update(stock=F('stock') + quantity)

        LOGGER.info(f"库存转移成功: {from_product_id} -> {to_product_id}, 数量: {quantity}")
        return {
            "from_product": from_product.name,
            "to_product": to_product.name,
            "quantity": quantity
        }

    async def get_product_statistics(self) -> Dict[str, Any]:
        """获取商品统计信息"""
        # 测试 aggregate 方法
        stats = await self.aggregate(
            Q(state=0),
            total_stock=Sum("stock"),
            avg_price=Avg("price"),
            max_price=Max("price"),
            min_price=Min("price"),
            product_count=Count("id")
        )
        return stats

    async def get_category_group_stats(self) -> List[Dict[str, Any]]:
        """按分类分组统计"""
        # 测试 group_by 方法
        results = await self.group_by(
            "category_id",
            Q(state=0),
            product_count=Count("id"),
            avg_price=Avg("price"),
            total_stock=Sum("stock")
        )
        return results
