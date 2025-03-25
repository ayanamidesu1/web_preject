import uuid
import os
from io import BytesIO

from PIL import Image, ImageOps
from django.db import connection
from django.views import View
from django.http import JsonResponse
from ..log.log import Logger
from datetime import datetime
import json

class UpdateUserBack(View):
    logger = Logger()
    target_path = 'H:/web_project/image/'
    thumbnail_path = 'H:/web_project/image/content_thumbnail/'
    allowed_formats = {
        'jpg': b'\xff\xd8\xff', 'jpeg': b'\xff\xd8\xff',
        'png': b'\x89PNG\r\n', 'tiff': b'II*\x00', 'webp': b'RIFF\x00\x00\x00\x00WEBP'
    }
    max_file_size = 8 * 1024 * 1024  # 最大文件容量 8MB

    def request_path(self, request):
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        request_ip = request.META.get('REMOTE_ADDR', 'unknown')
        return f'{request_ip}在{now}请求了{request.path}'

    def create_uuid(self):
        return str(uuid.uuid4())

    def validate_image_format(self, file):
        """验证文件格式是否允许"""
        header = file.read(1024)
        file.seek(0)  # 重置文件指针
        for ext, magic in self.allowed_formats.items():
            if header.startswith(magic):
                return ext
        return None

    def validate_file_size(self, file):
        """验证文件大小是否超出限制"""
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)  # 重置文件指针
        return size <= self.max_file_size

    def process_image(self, file, width, height, ext):
        """处理图像，缩放并返回内存文件"""
        img = Image.open(file)
        img = img.convert('RGB') if img.mode == 'RGBA' else img
        img.thumbnail((width, height), Image.LANCZOS)  # 缩放图片保持比例
        buffer = BytesIO()
        img.save(buffer, format=ext.upper(), quality=100)  # 使用明确的格式保存图像
        buffer.seek(0)
        return buffer

    def save_to_file(self, file, target_path):
        """保存文件到指定路径"""
        try:
            os.makedirs(os.path.dirname(target_path), exist_ok=True)  # 确保目录存在
            with open(target_path, 'wb') as f:
                f.write(file.read())
            return True
        except Exception as e:
            self.logger.error(f'文件保存失败，错误信息为：{e}')
            return False

    def post(self, request, *args, **kwargs):
        try:
            files = request.FILES.getlist('files')
            userid = getattr(request, 'userid', None)

            if not files or not userid:
                return JsonResponse({'status': 'error', 'message': '用户ID或文件为空'}, status=400)

            saved_files = []
            for file in files:
                if not self.validate_file_size(file):
                    return JsonResponse({'status': 'file_error', 'message': '文件超出大小限制'}, status=400)

                ext = self.validate_image_format(file)
                if ext not in self.allowed_formats:
                    return JsonResponse({'status': 'file_error', 'message': '文件格式不允许'}, status=400)

                # 生成唯一文件名
                filename = self.create_uuid() + '.' + ext

                # 保存原文件
                file_path = os.path.join(self.target_path, filename)
                if self.save_to_file(file, file_path):
                    saved_files.append(filename)

                # 生成缩略图并保存
                thumbnail = self.process_image(file, 1920, 1080, ext)  # 传递扩展名
                thumbnail_path = os.path.join(self.thumbnail_path, filename)  # 修正路径拼接
                if self.save_to_file(thumbnail, thumbnail_path):
                    saved_files.append(filename)

            if saved_files:
                with connection.cursor() as cursor:
                    cursor.execute('UPDATE users SET user_back_img=%s WHERE userid=%s', [saved_files[-1], userid])
                    if cursor.rowcount >= 1:
                        return JsonResponse({'status': 'success', 'message': '上传成功'}, status=200)

            return JsonResponse({'status': 'error', 'message': '上传失败'}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': f'数据解析失败: {e}'}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': f'服务器错误: {e}'}, status=500)
