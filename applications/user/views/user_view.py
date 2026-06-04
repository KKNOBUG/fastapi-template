# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : KeenRunner Template
@Module  : user_view.py
@DateTime: 2025/1/18 10:28
"""
import traceback

from fastapi import APIRouter, Body, Query
from tortoise.expressions import Q

from applications.user.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserSelect,
    UpdatePassword,
    UserBatchDelete
)
from applications.user.services.user_crud import USER_CRUD
from configure import LOGGER
from core.exceptions import DataAlreadyExistsException, NotFoundException
from core.responses import (
    NotFoundResponse,
    SuccessResponse,
    FailureResponse,
    DataAlreadyExistsResponse,
)
from services import CTX_USER_ID, DependAuth, verify_password, get_password_hash

user = APIRouter()


@user.post("/create", summary="新增用户")
async def create_user(user_in: UserCreate = Body()):
    try:
        instance = await USER_CRUD.create_user(user_in=user_in)
        data = await instance.to_dict()
        return SuccessResponse(data=data)
    except DataAlreadyExistsException as e:
        return DataAlreadyExistsResponse(message=str(e))
    except Exception as e:
        return FailureResponse(message=f"新增失败，异常描述:{e}")


@user.delete("/delete", summary="删除用户", description="根据id删除用户信息")
async def delete_user(user_id: int = Query(..., description="用户ID")):
    try:
        instance = await USER_CRUD.delete_user(user_id)
        data = await instance.to_dict()
        return SuccessResponse(data=data)
    except NotFoundException as e:
        return NotFoundResponse(message=str(e))
    except Exception as e:
        return FailureResponse(message=f"删除失败，异常描述:{e}")


@user.post("/delete", summary="按id列表删除用户")
async def delete_user_batch(user_in: UserBatchDelete = Body(..., description="用户信息")):
    try:
        count = await USER_CRUD.delete_users(user_in=user_in)
        LOGGER.info(f"按id列表删除用户成功, 数量: {count}")
        return SuccessResponse(message="删除成功", data={"affected": count}, total=count)
    except Exception as e:
        LOGGER.error(f"按id列表删除用户失败，异常描述: {e}\n{traceback.format_exc()}")
        return FailureResponse(message=f"删除失败, 异常描述: {e}")


@user.post("/update", summary="更新用户", description="根据id更新用户信息")
async def update_user(user_in: UserUpdate = Body(..., description="用户信息")):
    user_id: int = user_in.id
    try:
        instance = await USER_CRUD.update_user(user_in)
        data = await instance.to_dict()
        return SuccessResponse(data=data)
    except NotFoundException as e:
        return NotFoundResponse(message=str(e))
    except Exception as e:
        return FailureResponse(message=f"更新失败，异常描述:{e}")


@user.get("/get", summary="查询用户信息", description="根据id查询用户信息")
async def get_user(user_id: int = Query(..., description="用户ID")):
    instance = await USER_CRUD.get_by_id(user_id=user_id)
    if not instance:
        return NotFoundResponse(message=f"用户(id={user_id})信息不存在")
    data: dict = await instance.to_dict(exclude_fields=["password"])
    return SuccessResponse(data=data)


@user.get("/byUsername", summary="查询用户信息", description="根据用户名查询用户信息")
async def get_user_by_username(username: str = Query(..., description="用户名称")):
    instance = await USER_CRUD.model.filter(username=username).first()
    if not instance:
        return NotFoundResponse(message=f"用户(username={username})信息不存在")
    data: dict = await instance.to_dict(exclude_fields=["password"])
    return SuccessResponse(data=data)


@user.get("/list", summary="查询用户列表", description="支持分页按条件查询用户列表信息（Query）")
async def list_user(
        page: int = Query(default=1, ge=1, description="页码"),
        page_size: int = Query(default=10, ge=10, description="每页数量"),
        order: list = Query(default=["id"], description="排序字段"),
        username: str = Query(default=None, description="用户账号，用于搜索"),
        alias: str = Query(default=None, description="用户名称，用于搜索"),
        email: str = Query(default=None, description="邮箱地址"),
):
    q = Q()
    if username:
        q &= Q(username__contains=username)
    if alias:
        q &= Q(alias__contains=alias)
    if email:
        q &= Q(email__contains=email)
    q &= Q(state=0)
    total, user_objs = await USER_CRUD.list(page=page, page_size=page_size, order=order, search=q)
    data = [await obj.to_dict(exclude_fields=["password"]) for obj in user_objs]
    return SuccessResponse(data=data, total=total)


@user.post("/search", summary="查询用户列表", description="支持分页按条件查询用户列表信息（Body）")
async def get_users(user_in: UserSelect = Body()):
    q = Q()
    if user_in.username:
        q &= Q(username__contains=user_in.username)
    if user_in.alias:
        q &= Q(alias__contains=user_in.alias)
    if user_in.email:
        q &= Q(email__contains=user_in.email)
    if user_in.phone:
        q &= Q(phone__contains=user_in.phone)
    if user_in.is_active is not None:
        q &= Q(is_active=user_in.is_active)
    if user_in.is_superuser is not None:
        q &= Q(is_superuser=user_in.is_superuser)
    if user_in.state is not None:
        q &= Q(state=user_in.state)
    else:
        q &= Q(state=0)
    total, instances = await USER_CRUD.list(
        page=user_in.page, page_size=user_in.page_size, search=q, order=user_in.order
    )
    data = [await obj.to_dict(exclude_fields=["password"]) for obj in instances]
    return SuccessResponse(data=data, total=total)


@user.post("/update_password", summary="修改密码", dependencies=[DependAuth])
async def update_user_password(req_in: UpdatePassword):
    user_id = CTX_USER_ID.get()
    instance = await USER_CRUD.get(user_id)
    verified = verify_password(req_in.old_password, instance.password)
    if not verified:
        return FailureResponse(message="旧密码验证错误")
    instance.password = get_password_hash(req_in.new_password)
    await instance.save()
    return SuccessResponse(message="修改成功")


@user.post("/reset_password", summary="重置密码")
async def reset_password(user_id: int = Body(..., description="用户ID", embed=True)):
    data = await USER_CRUD.reset_password(user_id)
    return SuccessResponse(data=data)
