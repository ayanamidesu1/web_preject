import json
import uuid
from io import BytesIO

from PIL import Image, ImageOps
from django.db import connection, transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from datetime import datetime
from typing import Optional, List, Dict, Union
from log.log import Logger

logger = Logger()


class BaseApi(View):
    """RESTful API 基类，提供通用功能"""

    def get_client_ip(self, request) -> str:
        """安全获取客户端 IP（处理代理）"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
        ips = [ip.strip() for ip in x_forwarded_for.split(',') if ip.strip()]
        if ips:
            client_ip = ips[0]
        else:
            client_ip = request.META.get('REMOTE_ADDR', 'unknown')
        return f"{client_ip} @ {datetime.now().isoformat()}"

    def get_now(self):
        return datetime.now()

    def get_uuid(self):
        return str(uuid.uuid4())

    def log_request(self, request, level='info'):
        """记录请求日志"""
        msg = f"Request: {request.method} {request.path} - {self.get_client_ip(request)}"
        logger.warning(msg)

    def info_log(self, msg, request):
        logger.info(f'{msg}，请求时间：{datetime.now().isoformat()}，请求IP：{self.get_client_ip(request)}')

    def warning_log(self, msg, request):
        logger.warning(f'{msg}，请求时间：{datetime.now().isoformat()}，请求IP：{self.get_client_ip(request)}')

    def error_log(self, msg, request):
        logger.error(f'{msg}，请求时间：{datetime.now().isoformat()}，请求IP：{self.get_client_ip(request)}')

    def http_method_not_allowed(self, request, *args, **kwargs):
        """处理未允许的 HTTP 方法"""
        self.log_request(request, 'warning')
        return JsonResponse(
            {'code': 405, 'msg': 'Method Not Allowed'},
            status=405
        )

    def check_admin(self, request):
        """检查管理员权限，否代表通过，是直接返回错误消息"""
        if not request.user.is_login and request.user.role not in ['admin', 'sys_admin']:
            return JsonResponse({'code': 403, 'msg': "权限问题"}, status=403)
        return False

    def check_user(self, request):
        """检查用户权限，否代表通过，是直接返回错误消息"""
        if not request.user.is_login:
            return JsonResponse({'code': 401, 'msg': "用户未登录"}, status=401)
        return False

    @transaction.atomic
    def execute_sql(
            self,
            sql: str,
            params: Optional[list] or Optional[tuple] = None,
            return_results: bool = True
    ) -> Union[List[Dict], int, None]:
        """
        执行 SQL 语句，支持查询与更新

        :param return_results: 是否返回查询结果（SELECT时使用）
        :param params:传入的SQL参数，可选为列表或元组
        :return: 查询返回字典列表/更新返回影响行数/出错返回None
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)

                if return_results and cursor.description:
                    # 处理查询结果
                    columns = [col[0] for col in cursor.description]
                    return [dict(zip(columns, row)) for row in cursor.fetchall()]
                else:
                    # 处理 INSERT/UPDATE 等
                    return cursor.rowcount

        except Exception as e:
            logger.error(
                f"SQL Error: {e}\n"
                f"SQL: {sql}\n"
                f"Params: {params}"
            )
            raise  # 抛出异常供上层处理

    def execute_sql_many(self, sql, params_list):
        """执行批量SQL操作"""
        with connection.cursor() as cursor:
            cursor.executemany(sql, params_list)
            return cursor.rowcount

    def is_login(self, request) -> Union[JsonResponse, bool]:
        user = request.user
        if not user.is_login:
            return JsonResponse({'code': 400, 'msg': 'token失效或为空'}, status=400)
        else:
            return True

    def post(self, request, *args, **kwargs) -> JsonResponse:
        """示例 POST 处理，应由子类重写"""
        self.log_request(request)
        return JsonResponse(
            {'code': 405, 'msg': 'Method Not Allowed'},
            status=405
        )

    def get(self, request, *args, **kwargs) -> JsonResponse:
        logger.warning(f'非法get请求，请求时间：{datetime.now().isoformat()}，请求IP：{self.get_client_ip(request)}')
        return render(request, '404.html')

    def save_file(self, path, file):
        """通用文件写入函数"""
        try:
            with open(path, 'wb') as f:
                # 判断是否为分片对象（如 Django 的 UploadedFile）
                if hasattr(file, 'chunks'):
                    for chunk in file.chunks():
                        f.write(chunk)
                else:
                    # 处理原始字节数据（如 bytes 或 BytesIO）
                    if isinstance(file, bytes):
                        f.write(file)
                    else:
                        # 假设 file 是文件对象（如 open() 返回的文件流）
                        f.write(file.read())
        except Exception as e:
            logger.error(f"文件写入失败，错误信息：{e}")
            return False
        return True

    def format_request(self, request) -> Union[bool, dict]:
        """格式化请求数据
            :param request:  传入请求，格式化请求数据
            :return: 返回格式化后的数据，或者格式化失败信息
        """
        try:
            data = json.loads(request.body.decode('utf-8'))
            return data
        except Exception as e:
            logger.error("格式化请求失败")
            return False

    def format_file_request(self, request, file_name='file', data_name='data') -> Union[bool, dict]:
        """格式化文件请求数据
            :param request: 传入请求，格式化请求数据
            :return 返回格式化后的数据，或者格式化失败信息
        """
        try:
            file = request.FILES.get(file_name)
            data = request.POST.get(data_name)
            try:
                data = json.loads(data)
            except Exception as e:
                logger.error(f"格式化请求失败,{self.error_log(e, request)}")
                return False
            return {'file': file, 'data': data}
        except Exception as e:
            logger.error(f"格式化请求失败,{self.error_log(e, request)}")
            return False

    def img_file_convert(self, file, width, height):
        img = Image.open(file)
        original_format = img.format  # 获取原始图像格式
        img_width, img_height = img.size
        aspect_ratio = img_width / img_height

        if img_width > 300 and img_height > 300:
            # 当图像宽高都大于300时，优先进行缩放
            if img_width > width or img_height > height:
                if img_width >= img_height:
                    new_width = width
                    new_height = int(new_width / aspect_ratio)
                else:
                    new_height = height
                    new_width = int(new_height * aspect_ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)

                # 如果缩放后的宽高仍然大于目标宽高，则进行裁切
                if new_width > width or new_height > height:
                    img = ImageOps.fit(img, (width, height), Image.LANCZOS, 0.5, (0.5, 0.5))
            else:
                # 如果宽高都小于目标尺寸，按最大边进行裁切
                img = ImageOps.fit(img, (width, height), Image.LANCZOS, 0.5, (0.5, 0.5))
        else:
            # 当图像宽高小于300时，裁切和缩放同等优先级
            if img_width >= width and img_height >= height:
                img = ImageOps.fit(img, (width, height), Image.LANCZOS, 0.5, (0.5, 0.5))
            elif img_width >= width or img_height >= height:
                target_size = max(width, height)
                if img_width > img_height:
                    new_height = target_size
                    new_width = int(new_height * aspect_ratio)
                else:
                    new_width = target_size
                    new_height = int(new_width / aspect_ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)
                img = ImageOps.fit(img, (width, height), Image.LANCZOS, 0.5, (0.5, 0.5))
            else:
                if img_width >= img_height:
                    new_width = width
                    new_height = int(new_width / aspect_ratio)
                else:
                    new_height = height
                    new_width = int(new_height * aspect_ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)
                # 确保宽高小于300时进行裁切
                if new_width < 300 or new_height < 300:
                    img = ImageOps.fit(img, (max(new_width, 300), max(new_height, 300)), Image.LANCZOS, 0.5, (0.5, 0.5))

        if img.mode == 'RGBA':
            img = img.convert('RGB')

        buffer = BytesIO()
        img.save(buffer, format=original_format, quality=100)
        buffer.seek(0)
        return buffer
