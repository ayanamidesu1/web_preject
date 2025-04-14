from django.http import JsonResponse
from base_api import BaseApi
from django.conf import settings
import os
from datetime import datetime
import json
import magic


class CompleteWork(BaseApi):
    def __init__(self):
        super().__init__()
        self.file_path = 'upload_file'
        self.allowed_mime_types = [
            # 图像类
            'image/png', 'image/jpeg', 'image/gif', 'image/bmp', 'image/webp',
            # PSD
            'application/octet-stream',  # Photoshop 通常为 application/octet-stream
            # 压缩包
            'application/zip', 'application/x-rar-compressed',
            'application/x-7z-compressed', 'application/x-tar',
            'application/gzip'
        ]

    def is_valid_file(self, file):
        mime = magic.from_buffer(file.read(2048), mime=True)
        file.seek(0)  # 读取后要重置读取位置
        return mime in self.allowed_mime_types

    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if self.check_user(request):
                return self.check_user(request)

            file = request.FILES.get('file')
            data = json.loads(request.POST.get('data'))

            if not file or not data:
                return JsonResponse({"code": 400, "msg": "缺少参数"}, status=400)

            if not self.is_valid_file(file):
                return JsonResponse({"code": 400, "msg": "不支持的文件类型"}, status=400)

            ext = os.path.splitext(file.name)[1].lower()
            file_name = self.get_uuid() + ext
            file_path = os.path.join(settings.BASE_DIR,'static', self.file_path, file_name)
            now = datetime.now()

            sql = '''
                INSERT INTO work_order (user_id, target_user_id, time, file, order_id)
                VALUES (%s, %s, %s, %s, %s)
            '''
            update_order_status_sql = '''
                UPDATE `order` SET status = 4 WHERE id = %s
            '''

            if self.save_file(file_path, file):
                if self.execute_sql(sql, [
                    request.user.id,
                    data.get('target_user_id', data.get('order_id')),
                    now,
                    file_name,
                    data.get('order_id')
                ]) == 1:
                    if self.execute_sql(update_order_status_sql, [data.get('order_id')]) == 1:
                        return JsonResponse({"code": 200, "msg": "提交成功"}, status=200)
                    else:
                        return JsonResponse({"code": 500, "msg": "更新订单状态失败"}, status=500)
                else:
                    return JsonResponse({"code": 500, "msg": "数据库服务器错误"}, status=500)
            else:
                return JsonResponse({"code": 500, "msg": "服务器保存文件错误"}, status=500)

        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({"code": 500, "msg": "服务器内部错误"}, status=500)
