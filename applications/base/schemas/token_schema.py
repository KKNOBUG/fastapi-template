# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : Krun
@Module  : token_schema.py
@DateTime: 2025/1/18 12:07
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CredentialsSchema(BaseModel):
    username: str = Field(..., description="用户账号[用户工号或手机号码]")
    password: str = Field(..., description="用户密码[a-zZ-Z0-9_-.*@!]")


class JWTOut(BaseModel):
    access_token: str = Field(..., description="访问令牌")
    username: str = Field(..., description="用户账号")
    alias: str = Field(..., description="用户姓名")
    email: str = Field(..., description="用户邮箱")
    phone: Optional[str] = Field(default=None, description="用户电话")
    motto: Optional[str] = Field(default=None, description="用户签名")
    avatar: Optional[str] = Field(default=None, description="用户头像")
    address: Optional[str] = Field(default=None, description="用户住址")
    gender: int = Field(default=0, le=2, description="用户性别: 0未知 1男 2女")
    user_type: int = Field(default=0, le=9, description="用户类型：0xx 1xx 2xx")
    emergency_name: Optional[str] = Field(default=None, description="紧急联系人")
    emergency_phone: Optional[str] = Field(default=None, description="紧急联系电话")
    state: int = Field(default=0, description="状态(0:启用, 1:禁用)")
    is_active: bool = Field(default=True, description="是否激活")
    is_superuser: bool = Field(default=False, description="是否为超级管理员")
    last_login: Optional[datetime] = Field(default=None, description="最后一次登陆时间")


class JWTPayload(BaseModel):
    user_id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户账号")
    state: int = Field(default=0, description="状态(0:启用, 1:禁用)")
    is_superuser: bool = Field(default=False, description="是否为超级管理员")
    token_version: int = Field(default=0, description="Token版本号")
    exp: datetime = Field(..., description="过期时间")
