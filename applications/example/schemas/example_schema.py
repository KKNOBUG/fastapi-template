# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : example_schema.py
@DateTime: 2025/6/7
"""
from decimal import Decimal
from typing import Optional, List
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class CategoryBase(BaseModel):
    name: Optional[str] = Field(default=None, max_length=64, description="分类名称")
    code: Optional[str] = Field(default=None, max_length=32, description="分类编码")
    description: Optional[str] = Field(default=None, description="分类描述")
    sort_order: Optional[int] = Field(default=None, description="排序序号")
    parent_id: Optional[int] = Field(default=None, description="父分类ID")
    state: Optional[int] = Field(default=None, le=1, description="状态")


class CategoryCreate(CategoryBase):
    name: str = Field(..., max_length=64, description="分类名称")
    code: str = Field(..., max_length=32, description="分类编码")
    sort_order: int = Field(default=0, description="排序序号")
    state: int = Field(default=0, le=1, description="状态")

    def create_dict(self):
        return self.model_dump(exclude_unset=True)


class CategoryUpdate(CategoryBase):
    category_id: int = Field(..., description="分类ID")


class CategorySelect(CategoryBase):
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=10, ge=10, description="每页数量")
    order: Optional[list] = Field(default=["-sort_order"], description="排序字段")


class ProductBase(BaseModel):
    name: Optional[str] = Field(default=None, max_length=128, description="商品名称")
    code: Optional[str] = Field(default=None, max_length=32, description="商品编码")
    description: Optional[str] = Field(default=None, description="商品描述")
    price: Optional[Decimal] = Field(default=None, ge=0, description="商品价格")
    stock: Optional[int] = Field(default=None, ge=0, description="库存数量")
    category_id: Optional[int] = Field(default=None, description="分类ID")
    is_featured: Optional[bool] = Field(default=None, description="是否推荐")
    tags: Optional[List[str]] = Field(default=None, description="商品标签")
    state: Optional[int] = Field(default=None, le=1, description="状态")


class ProductCreate(ProductBase):
    name: str = Field(..., max_length=128, description="商品名称")
    code: str = Field(..., max_length=32, description="商品编码")
    price: Decimal = Field(..., ge=0, description="商品价格")
    stock: int = Field(default=0, ge=0, description="库存数量")
    category_id: int = Field(..., description="分类ID")
    state: int = Field(default=0, le=1, description="状态")
    uid: Optional[str] = Field(default=None, description="UUID")

    @field_validator('uid', mode='before')
    @classmethod
    def generate_uid(cls, v):
        if v is None:
            return str(uuid4())
        return v

    def create_dict(self):
        return self.model_dump(exclude_unset=True)


class ProductUpdate(ProductBase):
    product_id: int = Field(..., description="商品ID")


class ProductSelect(ProductBase):
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=10, ge=10, description="每页数量")
    order: Optional[list] = Field(default=["-created_time"], description="排序字段")
    min_price: Optional[Decimal] = Field(default=None, ge=0, description="最低价格")
    max_price: Optional[Decimal] = Field(default=None, ge=0, description="最高价格")


class BatchCreateProducts(BaseModel):
    products: List[ProductCreate] = Field(..., description="商品列表")


class BatchUpdateProducts(BaseModel):
    updates: List[dict] = Field(..., description="更新数据列表")


class TransferStock(BaseModel):
    from_product_id: int = Field(..., description="转出商品ID")
    to_product_id: int = Field(..., description="转入商品ID")
    quantity: int = Field(..., gt=0, description="转移数量")
