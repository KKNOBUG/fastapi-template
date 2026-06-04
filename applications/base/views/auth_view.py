# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : KeenRunner Template
@Module  : auth_view.py
@DateTime: 2025/1/18 10:03
"""
from datetime import timedelta, datetime, timezone

from fastapi import APIRouter

from applications.base.schemas.token_schema import CredentialsSchema, JWTOut, JWTPayload
from applications.user.models.user_model import User
from applications.user.services.user_crud import USER_CRUD
from configure import PROJECT_CONFIG
from core.exceptions import NotFoundException, NoPermissionException
from core.responses import SuccessResponse, NotFoundResponse
from services import CTX_USER_ID, DependAuth, create_access_token

auth_public = APIRouter()
auth_secure = APIRouter()


@auth_public.post("/access_token", summary="用户鉴权", description="验证用户密码和状态并生成令牌")
async def get_login_access_token(credentials: CredentialsSchema):
    try:
        user: User = await USER_CRUD.authenticate(credentials)
    except (NotFoundException, NoPermissionException) as e:
        return NotFoundResponse(message=str(e.message), data=credentials.model_dump())

    await USER_CRUD.update_last_login(user.id)
    access_token_expires = timedelta(minutes=PROJECT_CONFIG.AUTH_JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + access_token_expires

    data = JWTOut(
        access_token=create_access_token(
            data=JWTPayload(
                user_id=user.id,
                username=user.username,
                state=user.state,
                is_superuser=user.is_superuser,
                exp=expire,
            )
        ),
        username=user.username,
        alias=user.alias,
        email=user.email,
        phone=user.phone,
        avatar=user.avatar,
        state=user.state,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        last_login=user.last_login
    )
    return SuccessResponse(data=data.model_dump())


@auth_secure.post("/userinfo", summary="查看用户信息", dependencies=[DependAuth])
async def get_userinfo():
    user_id = CTX_USER_ID.get()
    user_obj = await USER_CRUD.get(id=user_id)
    data = await user_obj.to_dict(exclude_fields=["password"])
    return SuccessResponse(data=data)
