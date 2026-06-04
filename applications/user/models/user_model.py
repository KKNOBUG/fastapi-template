# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : KeenRunner Template
@Module  : user_model.py
@DateTime: 2025/1/18 11:39
"""
from tortoise import fields

from applications.base.services.scaffold import ScaffoldModel, TimestampMixin, MaintainMixin, StateModel


class User(ScaffoldModel, StateModel, TimestampMixin, MaintainMixin):
    username = fields.CharField(max_length=32, unique=True, description="用户账号")
    password = fields.CharField(max_length=255, null=True, description="用户密码")
    alias = fields.CharField(max_length=64, index=True, description="用户姓名")
    email = fields.CharField(max_length=64, unique=True, description="用户邮箱")
    phone = fields.CharField(max_length=20, description="用户电话")
    avatar = fields.CharField(max_length=255, default=None, null=True, description="用户头像")
    is_active = fields.BooleanField(default=True, index=True, description="是否激活")
    is_superuser = fields.BooleanField(default=False, index=True, description="是否为超级管理员")
    last_login = fields.DatetimeField(null=True, index=True, description="最后一次登陆时间")

    class Meta:
        table = "krun_user"
