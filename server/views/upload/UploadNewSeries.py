import uuid
from io import BytesIO
from PIL import Image, ImageOps
from django.db import connection
from django.http import JsonResponse
from django.views import View
from datetime import datetime
import json
import os
import magic
from ..log.log import Logger

class UploadNewSeries(View):
    logger = Logger()

    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tiff'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
    cover_temp_path = 'H:/web_project/image/novel/temp_cover/'
    cover_target_path = 'H:/web_project/image/novel/'
    cover_thumbnail_path = 'H:/web_project/image/novel/thumbnail/'
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    sql = ('INSERT INTO novel_work(work_name, belong_to_username, belong_to_userid, work_series, work_tags, '
           'age_classification, work_cover, author_say, work_create_time, brief_introduction, work_status, '
           'original, category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

    def request_path(self, request):
        """
        获取请求的路径和时间信息
        """
        now = datetime.now()
        path = request.path
        request_ip = request.META.get('REMOTE_ADDR')
        return f'请求地址：{request_ip}， 请求时间：{now}，请求IP地址： {path}'

    def create_uuid(self):
        """
        生成一个新的UUID
        """
        return str(uuid.uuid4())

    @staticmethod
    def is_valid_file(file):
        """
        验证文件类型是否有效
        """
        mime = magic.Magic(mime=True)
        file_mime = mime.from_buffer(file.read(1024))
        file.seek(0)  # 将文件指针重置到文件开头
        return file_mime in ['image/jpeg', 'image/png', 'image/tiff']

    def get(self, request):
        """
        处理非法的GET请求
        """
        self.logger.info(self.request_path(request) + '非法访问' + '请求参数' + str(request.GET))
        return JsonResponse({'status': 'success', 'message': '非法访问'}, status=403)

    def post(self, request, *args, **kwargs):
        """
        处理POST请求，上传新的系列作品
        """
        try:
            files = request.FILES.getlist('file')
            work_info = request.POST.get('work_info')
            work_info=json.loads(work_info)
            cover_type = work_info.get('cover_type')
            token = work_info.get('token')
            userid=getattr(request,'userid',None)
            user_info = work_info.get('user_info')
            print(user_info)
            belong_to_user_id = user_info.get('userid')
            belong_to_username = user_info.get('username')

            tags = work_info.get('tags')
            str_tag = ','.join(tags)

            if cover_type == 'default_cover':
                user_choose_cover_path = work_info.get('user_choose_cover_path')
                src = 'https://www.sunyuanling.com/image/novel/temp_cover/'
                try:
                    file_name = os.path.basename(user_choose_cover_path.replace(src, ''))
                    temp_file_path = self.cover_temp_path + file_name
                    final_file_path = self.cover_target_path + file_name
                    self.move_file(temp_file_path, final_file_path)
                    thumbnail_path = self.cover_thumbnail_path + file_name
                    self.generate_thumbnail(final_file_path, thumbnail_path)
                except Exception as e:
                    self.logger.error(self.request_path(request) + '文件不存在' + '请求参数' + request.POST)
                    print(e)
                    return JsonResponse({'status': 'error', 'message': '文件不存在'}, status=404)

                with connection.cursor() as cursor:
                    cursor.execute(self.sql, [work_info.get('work_name'), belong_to_username, userid,
                                              work_info.get('title'), str_tag, work_info.get('age_classification'),
                                              file_name, work_info.get('author_say'), self.now,
                                              work_info.get('introducation'), work_info.get('work_status'),
                                              work_info.get('is_original'), work_info.get('series_name')])

                    if cursor.rowcount == 0:
                        print('上传失败')
                        self.logger.error(self.request_path(request) + '上传失败' + '请求参数' + request.POST)
                        return JsonResponse({'status': 'error', 'message': '上传失败'}, status=500)
                    print('上传成功')
                    return JsonResponse({'status': 'success', 'message': '上传成功'})

            elif cover_type == 'custom_cover':
                file_name = self.create_uuid() + 'custom_cover.jpg'
                final_file_path = self.cover_target_path + file_name
                self.save_file(files[0], final_file_path)
                thumbnail_path = self.cover_thumbnail_path + file_name
                self.generate_thumbnail(final_file_path, thumbnail_path)
                with connection.cursor() as cursor:
                    cursor.execute(self.sql, [work_info.get('work_name'), belong_to_username, userid,
                                              work_info.get('title'), str_tag, work_info.get('age_classification'),
                                              file_name, work_info.get('author_say'), self.now,
                                              work_info.get('introducation'), work_info.get('work_status'),
                                              work_info.get('is_original'), work_info.get('series_name')])
                    if cursor.rowcount == 0:
                        print('上传失败')
                        self.logger.error(self.request_path(request) + '上传失败' + '请求参数' + request.POST)
                        return JsonResponse({'status': 'error', 'message': '上传失败'}, status=500)
                    print('上传成功')
                    return JsonResponse({'status': 'success', 'message': '上传成功'})

            return JsonResponse({'status': 'success', 'message': '上传成功'})

        except json.JSONDecodeError as e:
            self.logger.error(self.request_path(request) + '请求参数错误' + '请求参数' + work_info+str(e))
            print(e)
            return JsonResponse({'status': 'error', 'message': '请求参数错误'}, status=400)
        except Exception as e:
            self.logger.error(self.request_path(request) + '服务器错误' + '错误信息' + str(e))
            print(e)
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)

    def generate_thumbnail(self, original_path, thumbnail_path, size=(200, 200)):
        """
        生成缩略图
        """
        with Image.open(original_path) as img:
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(thumbnail_path, format='JPEG', quality=95)

    def save_file(self, file, path):
        """
        保存文件到指定路径
        """
        with open(path, 'wb') as f:
            f.write(file.read())

    def move_file(self, src, dst):
        """
        移动临时文件到指定文件夹
        """
        os.rename(src, dst)
