import json
import os

from django.http import JsonResponse
from base_api import BaseApi
from format_img import ReWriteImg
from django.conf import settings


class register(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            file_name = f"{self.get_uuid()}.png"
            path=os.path.join(settings.BASE_DIR,'static','img',file_name)
            thumbnail_path=os.path.join(settings.BASE_DIR,'static','avatar_thumbnail',file_name)
            file=request.FILES.get('file')
            if file is None:
                return JsonResponse({'code':400,'msg':'请上传文件'},status=400)

            data=json.loads(request.POST.get('data'))
            if data is None:
                return JsonResponse({'code':400,'msg':'请输入数据'},status=400)
            sql='''
            select 1 from users where username=%s
            '''
            result=self.execute_sql(sql,[data.get('username')])
            if result is not None:
                return JsonResponse({'code':400,'msg':'用户名已存在'},status=400)
            format_img = ReWriteImg(file=file)
            img = format_img.copy_paste()
            thumbnail_file = self.img_file_convert(img, width=200, height=200)
            self.save_file(path, img)
            self.save_file(thumbnail_path, thumbnail_file)
            sql='''
            insert into users (username,password,user_avatar,email,phone,sex,vip,account_status,account_permissions,
            user_register,per,last_login,ip_address,role,userid) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            result=self.execute_sql(sql,[
                data.get('username'),data.get('password'),file_name,data.get('email'),
                data.get('phone'),data.get('sex'),0,1,0,self.get_now(),0,self.get_now(),self.get_client_ip(request),
                '用户',self.get_uuid()
            ])
            if result is None:
                return JsonResponse({'code':400,'msg':'注册失败'},status=400)
            if result==1:
                return JsonResponse({'code':200,'msg':'注册成功'},status=200)

            return JsonResponse({'code':200,'msg':'注册成功'},status=200)
        except Exception as e:
            self.error_log(e,request)
            return JsonResponse({'code':500,'msg':'服务器错误'},status=500)