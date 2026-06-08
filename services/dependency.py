# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : KeenRunner Template
@Module  : dependency.py
@DateTime: 2025/2/19 13:03
"""
from typing import Optional

import jwt
from fastapi import Depends, Header, HTTPException

from applications.user.models.user_model import User
from configure import PROJECT_CONFIG
from services import CTX_USER_ID


class AuthControl:
    @classmethod
    async def is_authed(cls, token: str = Header(..., description="token验证")) -> Optional["User"]:
        try:
            decode_data = jwt.decode(
                jwt=token,
                key=PROJECT_CONFIG.AUTH_SECRET_KEY,
                algorithms=PROJECT_CONFIG.AUTH_JWT_ALGORITHM
            )
            user_id = decode_data.get("user_id")
            user = await User.filter(id=user_id, state__not=1, is_active=True).first()
            if not user:
                raise HTTPException(status_code=401, detail="请求服务鉴权失败, 用户状态异常, 请联系管理员后重试")

            token_version = decode_data.get("token_version", 0)
            if token_version != user.token_version:
                raise HTTPException(status_code=401, detail="请求服务鉴权已过期, 请重新登录获取有效 Token 后进行访问")

            CTX_USER_ID.set(int(user_id))
            return user
        except jwt.DecodeError:
            raise HTTPException(status_code=401, detail="请求服务鉴权失败, 请携带有效 Token 进行访问")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="请求服务鉴权已过期, 请重新登录获取有效 Token 后进行访问")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{repr(e)}")


DependAuth = Depends(AuthControl.is_authed)
