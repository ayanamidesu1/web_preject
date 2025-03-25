import os
import json
import random
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageOps
from django.http import JsonResponse
from django.views import View
from django.db import connections, connection
import magic
from asgiref.sync import sync_to_async
from djangoWebServer.log.log import Logger
from config import settings
#from CoverHandle import CoverHandle

#cover_handle = CoverHandle()
class UploadFile(View):
    logger = Logger()

    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tiff'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

    def request_path(self, request):
        now = datetime.now()
        path = request.path
        request_ip = request.META.get('REMOTE_ADDR')
        return f'请求地址：{request_ip}， 请求时间：{now}，请求IP地址： {path}'

    @staticmethod
    def is_valid_file(file):
        mime = magic.Magic(mime=True)
        file_mime = mime.from_buffer(file.read(1024))
        file.seek(0)
        return file_mime in ['image/jpeg', 'image/png', 'image/tiff']

    def get(self, request, *args, **kwargs):
        self.logger.warning(self.request_path(request) + ' get非法访问 ' + str(request.GET))
        return JsonResponse({'status': 'error', 'message': '非法访问'}, status=403)

    def post(self, request, *args, **kwargs):
        try:
          pass

        except json.JSONDecodeError as e:
            #self.logger.error(self.request_path(request) + ' ' + str(e) + ' ' + str(work_info))
            return JsonResponse({'status': 'error', 'message': 'JSON格式错误'}, status=400)
        except Exception as e:
            #self.logger.error(self.request_path(request) + ' ' + str(e) + ' ' + str(work_info))
            print(e)
            return JsonResponse({'status': 'error', 'message': '服务器内部错误'}, status=500)

    def handle_upload(self, work_type, files, work_info, request, tag_list):
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        save_path, save_thumbnail_path = settings['paths'][work_type]
        content_file_list = []
        unique_prefix = self.generate_unique_prefix()

        for index, file in enumerate(files):
            filename, ext = os.path.splitext(file.name)
            if ext.lower() not in self.ALLOWED_EXTENSIONS:
                self.logger.error(f'文件类型不被允许: {file.name}')
                continue
            if file.size > self.MAX_FILE_SIZE:
                self.logger.error(f'文件过大: {file.name}')
                continue

            safe_filename = self.get_safe_filename(unique_prefix, index, ext)
            full_file_path = os.path.join(save_path, safe_filename)
            processed_image = self.process_image(file)
            self.save_file(full_file_path, processed_image)
            content_file_list.append(safe_filename)

            img_thumbnail = self.img_file_convert(file, 200, 200)
            thumbnail_path = os.path.join(save_thumbnail_path, safe_filename)
            self.save_file(thumbnail_path, img_thumbnail)

            #生成内容页的长宽最大1200的缩略图
            img_content = self.img_file_convert(file, 1200, 1200)
            content_path = os.path.join(save_path+'content_thumbnail/', safe_filename)
            self.save_file(content_path, img_content)

        content_file_list_str = ','.join(content_file_list)
        self.save_to_db(work_type, work_info, content_file_list_str, now, tag_list)
        self.logger.info(self.request_path(request) + ' 上传成功')

    def generate_unique_prefix(self):
        return ''.join(random.choices('0123456789', k=16))

    def get_safe_filename(self, unique_prefix, index, ext):
        return f"{unique_prefix}_p{index + 1}{ext}"

    def save_file(self, path, content):
        with open(path, 'wb') as f:
            f.write(content.read() if hasattr(content, 'read') else content)

    def save_to_db(self, work_type, work_info, content_file_list_str, now, tag_list):
        if work_type == 'ill':
            query = settings['queries']['ill']
            params = (
                work_info['name'], content_file_list_str, work_info['username'],
                work_info['userid'], tag_list, now,
                work_info['brief_introduction'], work_info['age_classification']
            )
        elif work_type == 'comic':
            query = settings['queries']['comic']
            params = (
                work_info['name'], content_file_list_str, work_info['username'],
                work_info['userid'], now, tag_list,
                work_info['age_classification'], work_info['brief_introduction']
            )
        elif work_type == 'novel':
            #temp_path=cover_handle.handle(work_info['name'],None,work_info['template_index'])
            query = settings['queries']['novel']
            params = (
                work_info['name'], content_file_list_str, work_info['username'],
                work_info['userid'], now, work_info.get('work_series', ''), tag_list,
                work_info['brief_introduction'], work_info.get('author_say', ''),
                work_info['age_classification'], work_info.get('work_status', '')
            )
        else:
            raise ValueError(f"Unsupported work_type: {work_type}")

        with connections['default'].cursor() as cursor:
            cursor.execute(query, params)

    def process_image(self, file):
        img = Image.open(file)
        original_format = img.format  # 获取原始图像格式
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        # 保持原有渲染方式并使用 LANCZOS 滤镜
        img = img.resize(img.size, Image.LANCZOS)
        buffer = BytesIO()
        img.save(buffer, format=original_format, quality=100, subsampling=0)
        buffer.seek(0)
        return buffer

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

os_path = 'H:/web_project/image/comic/'
target_path = 'H:/web_project/image/comic/content_thumbnail/'

# 创建 UploadFile 实例
uploadfile = UploadFile()

# 遍历文件夹生成内容页缩略图
for file in os.listdir(os_path):
    if file.lower().endswith(('.jpg', '.png', '.jpeg', '.tiff')):
        file_path = os.path.join(os_path, file)
        img = uploadfile.img_file_convert(file_path, 1200, 1200)

        # 确保目标路径存在
        os.makedirs(target_path, exist_ok=True)

        # 保存转换后的缩略图
        with open(os.path.join(target_path, file), 'wb') as f:
            f.write(img.read())

