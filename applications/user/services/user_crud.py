# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : KeenRunner Template
@Module  : user_crud.py
@DateTime: 2025/1/18 11:36
"""
from datetime import datetime
from typing import Optional, Union, List, Dict, Any

from tortoise.exceptions import DoesNotExist

from applications.base.schemas.token_schema import CredentialsSchema
from applications.base.services.scaffold import ScaffoldCrud
from applications.user.models.user_model import User
from applications.user.schemas.user_schema import UserCreate, UserUpdate, UserBatchDelete
from configure import LOGGER
from core.exceptions import (
    NotFoundException,
    BaseExceptions,
    DataAlreadyExistsException,
    ParameterException,
    NoPermissionException,
)
from core.responses import ForbiddenResponse
from services import verify_password, get_password_hash


class UserCrud(ScaffoldCrud[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(model=User)

    async def get_by_id(self, user_id: int, on_error: bool = False, is_active: bool = True) -> Optional[User]:
        if not user_id:
            error_message: str = "查询用户信息失败, 参数(user_id)不允许为空"
            LOGGER.error(error_message)
            raise ParameterException(message=error_message)
        kwargs: Dict[str, Any] = {"id": user_id}
        if is_active:
            kwargs["state__not"] = 1
        instance = await self.model.filter(**kwargs).first()
        if not instance and on_error:
            error_message: str = f"查询用户信息失败, 用户(id={user_id})不存在"
            LOGGER.error(error_message)
            raise NotFoundException(message=error_message)
        return instance

    async def get_by_username(self, username: str, on_error: bool = False, is_active: bool = True) -> Optional[User]:
        if not username:
            error_message: str = "查询用户信息失败, 参数(username)不允许为空"
            LOGGER.error(error_message)
            raise ParameterException(message=error_message)
        kwargs: Dict[str, Any] = {"username": username}
        if is_active:
            kwargs["state__not"] = 1
        instance = await self.model.filter(**kwargs).first()
        if not instance and on_error:
            error_message: str = f"查询用户信息失败, 用户(username={username})不存在"
            LOGGER.error(error_message)
            raise NotFoundException(message=error_message)
        return instance

    async def authenticate(self, credentials: CredentialsSchema) -> Optional[Union[BaseExceptions, User]]:
        user = await self.model.filter(username=credentials.username).first()
        if not user:
            raise NotFoundException(message="用户名不存在")
        verified = verify_password(credentials.password, user.password)
        if not verified:
            raise NotFoundException(message="用户名或密码错误")
        if user.state == 1:
            raise NoPermissionException(message="用户已禁用")
        return user

    async def update_last_login(self, id: int) -> None:
        user = await self.model.get(id=id)
        user.last_login = datetime.now()
        await user.save()

    async def create_user(self, user_in: UserCreate) -> User:
        username = user_in.username
        instances = await self.model.filter(username=username).all()
        if instances:
            raise DataAlreadyExistsException(message=f"用户(username={username})信息已存在")

        user_in.password = get_password_hash(password=user_in.password)
        return await self.create(user_in)

    async def delete_user(self, user_id: int) -> User:
        instance = await self.query(user_id)
        if not instance or instance.state != 0:
            raise NotFoundException(message=f"用户(id={user_id})信息不存在")

        instance.state = 1
        instance.is_active = False
        await instance.save()
        return instance

    async def delete_users(self, user_in: UserBatchDelete) -> Optional[List[int]]:
        user_ids: Optional[List[int]] = user_in.user_ids
        if user_ids:
            deleted_ids = await self.model.filter(id__in=user_ids).exclude(state=1).values_list("id", flat=True)
            if deleted_ids:
                await self.model.filter(id__in=deleted_ids).update(state=1)
        else:
            deleted_ids = None
        return deleted_ids

    async def update_user(self, user_in: UserUpdate) -> User:
        user_id: int = user_in.user_id
        user_if: dict = user_in.model_dump(exclude_unset=True, exclude_none=True)
        try:
            instance = await self.update(id=user_id, obj_in=user_if)
        except DoesNotExist:
            raise NotFoundException(message=f"用户(id={user_id})信息不存在")
        return instance

    async def reset_password(self, user_id: int):
        instance = await self.get(id=user_id)
        if instance.is_superuser:
            return ForbiddenResponse(message="不允许重置超级用户密码")

        instance.password = get_password_hash(password="123456")
        await instance.save()
        return await instance.to_dict(exclude_fields=["id", "password"])


USER_CRUD = UserCrud()
