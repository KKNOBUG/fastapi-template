# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : __init__.py
@DateTime: 2025/4/28 18:05
"""
import argparse, os
from dotenv import load_dotenv

from core.exceptions.base_exceptions import (
    NotFoundException,
    DataNotStandardizedException,
    ParameterException
)


class OverrideArgumentParserError(argparse.ArgumentParser):
    def error(self, message):
        raise ParameterException(
            message=f"参数输入有误: {message}，请检查参数名和参数值。[--env] 参数可选值为：[dev ｜ test ｜ prod]"
        )


def load_environment_file():
    # 创建一个参数解析器
    parser = OverrideArgumentParserError(description='启动项目')
    parser.add_argument(
        "--env",
        type=str,
        default='dev',
        choices=["dev", "test", "prod"],
        help="请指定环境，可选值为：[dev ｜ test ｜ prod]"
    )

    try:
        args = parser.parse_args()
        env_name = args.env
        env_root: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        env_file = os.path.join(env_root, f".env.{env_name}")
        # 检查.env文件是否存在
        if not os.path.exists(env_file):
            raise NotFoundException(message=f"指定的环境文件[{env_file}]不存在")
        # 加载.env文件中的环境变量，允许覆盖现有环境变量
        load_dotenv(env_file, override=True)
    except ParameterException as e:
        raise ParameterException(message=f"加载环境文件出现错误:{e.message}")
    except NotFoundException as e:
        raise NotFoundException(message=f"加载环境文件出现错误: {e.message}")
    except Exception as e:
        raise DataNotStandardizedException(message=f"加载环境文件出现错误:{e}")

    return env_name, env_file
