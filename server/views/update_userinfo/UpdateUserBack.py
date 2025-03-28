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
from django.conf import settings
from base_api import BaseApi
from format_img import ReWriteImg

class UpdateUserBack(BaseApi):
    def post(self, request, *args, **kwargs):
        try:
            files = request.FILES.getlist('files')
            userid = request.user.id

            if not files or not userid:
                return JsonResponse({'status': 'error', 'message': '用户ID或文件为空','code':400}, status=400)
            filename=f'{self.get_uuid()}.png'
            target_file_path=os.path.join(settings.BASE_DIR,'static','image',filename)
            thumbnail_file_path=os.path.join(settings.BASE_DIR,'static','image','content_thumbnail',filename)
            for file in files:
                re_write=ReWriteImg(file=file,width=1920,height=1080)
                file=re_write.copy_paste()
                thumbnail_file=re_write.process_image()
                self.save_file(target_file_path,file)
                self.save_file(thumbnail_file_path,thumbnail_file)
            sql='''
            update users set user_back_img=%s where userid=%s
            '''
            if self.execute_sql(sql,[filename,userid])==1:
                return JsonResponse({'code':200,'msg':'上传成功','status':'success'},status=200)
            return JsonResponse({'code':400,'msg':'上传失败','status':'error'},status=400)

        except Exception as e:
            print(e)
            self.error_log(e,request)
            return JsonResponse({'code':500,'msg':'服务器错误','status':'error'},status=500)