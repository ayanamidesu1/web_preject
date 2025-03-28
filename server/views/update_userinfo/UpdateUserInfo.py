import os
import uuid
from io import BytesIO

from django.db import connection
from django.http import JsonResponse
from django.views import View
from ..log.log import Logger
from datetime import datetime
import json
from PIL import Image, ImageOps
from django.conf import settings
from base_api import BaseApi
from format_img import ReWriteImg


class UpdateUserInfo(BaseApi):
    logger = Logger()
    target_path = os.path.join(settings.BASE_DIR, 'static', 'image')
    thumbnail_path = os.path.join(settings.BASE_DIR, 'static', 'image', 'content_thumbnail')
    allowed_formats = {'jpg': b'\xff\xd8\xff', 'jpeg': b'\xff\xd8\xff', 'png': b'\x89PNG\r\n', 'tiff': b'II*\x00',
                       'webp': b'RIFF\x00\x00\x00\x00WEBP'}
    max_file_size = 1024 * 1024 * 8  # 最大文件容量 8MB

    def request_path(self, request):
        request_path = request.path
        request_ip = request.META['REMOTE_ADDR']
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        return f'{request_ip}在{now}请求了{request_path}'

    def post(self, request, *args, **kwargs):
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        try:
            files = request.FILES.getlist('files')
            data = json.loads(request.POST.get('data', '{}'))
            userid = request.user.id

            with connection.cursor() as cursor:
                userinfo = data
                if not userinfo:
                    self.logger.warning(self.request_path(request) + '请求数据为：' + str(
                        request.POST) + '，错误信息为：' + 'userinfo为空')
                    return JsonResponse({'status': 'error', 'message': 'userinfo为空'}, status=400)

                filename = None
                cursor.execute('SELECT user_avatar FROM users WHERE userid=%s', [userid])
                filename = cursor.fetchone()[0]

                # 处理上传的文件
                if files:
                    for file in files:
                        re_write=ReWriteImg(file=file,width=200,height=200,max_size=10*1024*1024)
                        filename=f'{self.get_uuid()}.png'
                        if not re_write.check_file_size():
                           return JsonResponse({'status': 'error', 'message': '文件大小超过10MB'}, status=400)
                        if not re_write.is_safe_image():
                            return JsonResponse({'status': 'error', 'message': '文件格式错误'}, status=400)
                        target_path=os.path.join(settings.BASE_DIR,'static','image',filename)
                        avatar_thumbnail=os.path.join(settings.BASE_DIR,'static','image','avatar_thumbnail',filename)
                        file=re_write.copy_paste()
                        thumbnail_file=re_write.process_image()
                        if not self.save_file(target_path,file) or not self.save_file(avatar_thumbnail,thumbnail_file):
                            return JsonResponse({'status': 'error', 'message': '文件保存失败'}, status=500)

                # 更新用户信息
                sql = ('UPDATE users SET username=%s, user_self_introduction=%s, user_address=%s, birthday=%s,'
                       ' user_avatar=%s, user_self_website=%s, sex=%s WHERE userid=%s')
                cursor.execute(sql, [userinfo.get('username'), userinfo.get('user_self_introduction'),
                                     userinfo.get('user_address'), userinfo.get('birthday'),
                                     filename, userinfo.get('user_self_website'), userinfo.get('sex'), userid])

                return JsonResponse({'status': 'success', 'message': '更新成功'}, status=200)

        except json.JSONDecodeError as e:
            print(e)
            self.logger.warning(
                self.request_path(request) + '请求数据为：' + str(request.POST) + '，错误信息为：' + str(e))
            return JsonResponse({'status': 'error', 'message': '请求数据格式错误'}, status=400)
        except Exception as e:
            print(e)
            self.logger.error(self.request_path(request) + '请求数据为：' + str(request.POST) + '，错误信息为：' + str(e))
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)

    def validate_image_format(self, file, request):
        try:
            file.seek(0)
            header = file.read(1024)
            file.seek(-1024, os.SEEK_END)
            footer = file.read(1024)
            file.seek(0)  # 重置文件指针

            for ext, magic in self.allowed_formats.items():
                if header.startswith(magic) or footer.startswith(magic):
                    return ext

            return None
        except Exception as e:
            self.logger.error(self.request_path(request) + '格式验证失败，错误信息为：' + str(e))
            return None

    def validate_file_size(self, file, request):
        try:
            file.seek(0, os.SEEK_END)
            size = file.tell()
            file.seek(0)  # 重置文件指针
            if size > self.max_file_size:
                return False
            return True
        except Exception as e:
            self.logger.error(self.request_path(request) + '文件大小检查失败，错误信息为：' + str(e))
            return False

    def save_to_file(self, file, target_path, request):
        try:
            with open(target_path, 'wb') as f:
                f.write(file.read())
            return True
        except Exception as e:
            self.logger.error(self.request_path(request) + '文件保存失败，错误信息为：' + str(e))
            return False


    def img_file_convert(self, file, width, height):
        img = Image.open(file)
        original_format = img.format  # 获取原始图像格式
        img_width, img_height = img.size
        aspect_ratio = img_width / img_height

        if img_width > 300 and img_height > 300:
            if img_width > width or img_height > height:
                if img_width >= img_height:
                    new_width = width
                    new_height = int(new_width / aspect_ratio)
                else:
                    new_height = height
                    new_width = int(new_height * aspect_ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)

                if new_width > width or new_height > height:
                    img = ImageOps.fit(img, (width, height), Image.LANCZOS, 0.5, (0.5, 0.5))
            else:
                img = ImageOps.fit(img, (width, height), Image.LANCZOS, 0.5, (0.5, 0.5))
        else:
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
                if new_width < 300 or new_height < 300:
                    img = ImageOps.fit(img, (max(new_width, 300), max(new_height, 300)), Image.LANCZOS, 0.5, (0.5, 0.5))

        if img.mode == 'RGBA':
            img = img.convert('RGB')

        buffer = BytesIO()
        img.save(buffer, format=original_format, quality=100)
        buffer.seek(0)
        return buffer
