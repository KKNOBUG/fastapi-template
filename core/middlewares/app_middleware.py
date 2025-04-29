# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : Krun
@Module  : app_middleware.py
@DateTime: 2025/1/17 22:29
"""
import json
import time
from io import BytesIO
from typing import Dict, Any
from urllib.parse import unquote

from fastapi import Request, Response
from starlette.datastructures import FormData

from configure.project_config import PROJECT_CONFIG
from configure.global_config import GLOBAL_CONFIG
from configure.logging_config import logger as LOGGER


def is_upload_request(request: Request) -> bool:
    path: str = request.url.path.lower()
    content_type: str = request.headers.get("content-type", "")
    return "multipart/form-data" in content_type.lower() or path.startswith("upload") or path.endswith("upload")


def is_html_response(response: Response) -> bool:
    content_type: str = response.headers.get("content-type", "")
    return "text/html" in content_type.lower() or "application/xml" in content_type.lower()


def is_image_response(response: Response) -> bool:
    content_type: str = response.headers.get("content-type", "")
    return "image" in content_type.lower()


def is_download_response(response: Response) -> bool:
    content_disposition: str = response.headers.get("content-disposition", "")
    return "attachment" in content_disposition.lower()


def is_longtext_response(response: Response) -> bool:
    content_length: int = response.headers.get("content-length", 0)
    return int(content_length) > 5000


async def logging_middleware(request: Request, call_next):
    # 接口服务时间
    start_time = time.time()
    request_time: str = time.strftime(GLOBAL_CONFIG.DATETIME_FORMAT2, time.localtime(start_time))

    # 变量初始化
    request_body, response_body = b'', b''

    # 读取并保存原始请求体，重置请求流以便后续处理
    original_request_body: bytes = await request.body()
    request._body = original_request_body
    request._stream = BytesIO(original_request_body)

    # 判断是否为文件上传请求
    is_upload: bool = is_upload_request(request)
    if is_upload:
        form_data: Dict[str, Any] = {}
        original_form_data: FormData = await request.form()
        # 提取字段和文件信息
        for field_name, field_value in original_form_data.items():
            if hasattr(field_value, 'file'):
                form_data[field_name] = {
                    "filename": field_value.filename,
                    "content_type": field_value.content_type,
                    "size": field_value.size
                }
            else:
                form_data[field_name] = field_value

        # 重置流的位置到开头，确保后续处理能正确读取
        request_body = json.dumps(form_data, ensure_ascii=False).encode("utf-8")
        request._stream.seek(0)

    # 记录请求信息
    request_method: str = request.method
    request_router: str = request.url.path
    request_header: dict = dict(request.headers)
    request_client: str = request.client.host if request.client else "127.0.0.1"
    request_tags: str = GLOBAL_CONFIG.ROUTER_TAGS.get(request_router or "未定义", "未定义")
    request_summary: str = GLOBAL_CONFIG.ROUTER_SUMMARY.get(request_router or "未定义", "未定义")
    request_body: bytes = request_body if is_upload else original_request_body.decode("utf-8", errors="ignore")
    request_params: str = unquote(request.query_params.__str__())

    # 请求流传递并获取响应
    response = await call_next(request)

    # 判断是否管控响应
    is_download: bool = is_download_response(response)
    is_html: bool = is_html_response(response)
    is_image: bool = is_image_response(response)
    is_longtext: bool = is_longtext_response(response)

    response_header: dict = dict(response.headers)

    # 路由排除（静态文件&OpenApi文档）
    if not request_router.startswith("/static/") and request_router not in (
            '/',
            '/base/audit/list',
            PROJECT_CONFIG.APP_DOCS_URL,
            PROJECT_CONFIG.APP_REDOC_URL,
            PROJECT_CONFIG.APP_OPENAPI_URL,
    ):
        # 消费响应体
        if is_download:
            response_body = b"<FILE DOWNLOAD>"
        elif is_html:
            response_body = b"<HTML CONTENT>"
        elif is_image:
            response_body = b"IMAGE CONTENT"
        elif is_longtext:
            response_body = b"LONGTEXT CONTENT"
        else:
            body_chunks = []
            async for chunk in response.body_iterator:
                body_chunks.append(chunk)

            response_body = b"".join(body_chunks).decode("utf-8", errors="ignore")

            # 重置响应体
            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=response_header,
                media_type=response.media_type
            )

        # 接口服务结束时间
        end_time = time.time()
        response_time: str = time.strftime(GLOBAL_CONFIG.DATETIME_FORMAT2, time.localtime(end_time))
        response_elapsed = f"{end_time - start_time:.4f}s"

        # 记录日志
        audit_log: Dict[str, Any] = {
            "request_time": request_time,
            "request_tags": request_tags,
            "request_summary": request_summary,
            "request_method": request_method,
            "request_router": request_router,
            "request_client": request_client,
            "request_header": request_header,
            "request_params": request_body or request_params,
            "response_time": response_time,
            "response_header": response_header,
            "response_elapsed": response_elapsed
        }
        if isinstance(response_body, str):
            _response = json.loads(response_body)
            audit_log["response_code"] = _response.get("code", "")
            audit_log["response_message"] = _response.get("message", "")[:512]
            audit_log["response_body"] = response_body
            del _response

        request_message: str = f"\n> > > > > > > > > > > > > > > > > > > >\n" \
                               f"请求时间：{audit_log.get('request_time')}\n" \
                               f"请求模块：{audit_log.get('request_tags')}\n" \
                               f"请求接口：{audit_log.get('request_summary')}\n" \
                               f"请求方式：{audit_log.get('request_method')}\n" \
                               f"请求路由：{audit_log.get('request_router')}\n" \
                               f"请求来源：{audit_log.get('request_client')}\n" \
                               f"请求头部：{audit_log.get('request_header')}\n" \
                               f"请求参数：{audit_log.get('request_params')}\n" \
                               f"响应头部：{audit_log.get('response_header')}\n" \
                               f"响应代码：{audit_log.get('response_code')}\n" \
                               f"响应消息：{audit_log.get('response_message')}\n" \
                               f"响应参数：{audit_log.get('response_body')}\n" \
                               f"响应时间：{audit_log.get('response_time')}\n" \
                               f"响应耗时：{audit_log.get('response_elapsed')}\n" \
                               f"< < < < < < < < < < < < < < < < < < < < "

        LOGGER.info(request_message)

    return response
