# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : KeenRunner Template
@Module  : data_initialization.py
@DateTime: 2025/2/19 22:12
"""
from fastapi import FastAPI

from applications.example.services.init_data import init_example_data
from applications.user.services.init_data import init_database_user


async def init_database_table(app: FastAPI):
    await init_database_user()
    await init_example_data()
