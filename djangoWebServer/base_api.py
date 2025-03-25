import json
from django.db import connection, transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from datetime import datetime
from typing import Optional, List, Dict, Union
from djangoProject.log.log import Logger

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

    def format_file_request(self, request, file_name='file', data_name='data')->Union[bool, dict]:
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
