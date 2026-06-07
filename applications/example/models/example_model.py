# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : example_model.py
@DateTime: 2025/6/7
"""
from tortoise import fields

from applications.base.services.scaffold import (
    ScaffoldModel,
    StateModel,
    TimestampMixin,
    MaintainMixin,
    UUIDModel,
)


class Category(ScaffoldModel, StateModel, TimestampMixin, MaintainMixin):
    """商品分类模型"""
    name = fields.CharField(max_length=64, description="分类名称")
    code = fields.CharField(max_length=32, unique=True, description="分类编码")
    description = fields.TextField(null=True, description="分类描述")
    sort_order = fields.IntField(default=0, description="排序序号")
    parent_id = fields.BigIntField(null=True, description="父分类ID")

    class Meta:
        table = "krun_example_category"


class Product(ScaffoldModel, StateModel, TimestampMixin, MaintainMixin, UUIDModel):
    """商品模型"""
    name = fields.CharField(max_length=128, description="商品名称")
    code = fields.CharField(max_length=32, unique=True, description="商品编码")
    description = fields.TextField(null=True, description="商品描述")
    price = fields.DecimalField(max_digits=10, decimal_places=2, description="商品价格")
    stock = fields.IntField(default=0, description="库存数量")
    category_id = fields.BigIntField(index=True, description="分类ID")
    is_featured = fields.BooleanField(default=False, description="是否推荐")
    tags = fields.JSONField(default=list, description="商品标签")

    class Meta:
        table = "krun_example_product"
