import os.path
import json
from datetime import datetime

from django.db import transaction

from base_api import BaseApi
from django.http import JsonResponse
from format_img import ReWriteImg
from djangoWebServer.settings import BASE_DIR


class AddFunc(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.user.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录'}, status=401)

            user_id = request.user.id
            file = request.FILES.get('file')
            data_str = request.POST.get('data')

            if not file:
                return JsonResponse({'code': 400, 'msg': '文件为空'}, status=400)
            if not data_str:
                return JsonResponse({'code': 400, 'msg': '数据为空'}, status=400)

            try:
                data = json.loads(data_str)
            except json.JSONDecodeError:
                return JsonResponse({'code': 400, 'msg': '数据格式错误'}, status=400)

            # 验证必要字段
            required_fields = ['title', 'work_type', 'age_classification',
                               'introduce', 'tags', 'amount_of_money']
            if not all(field in data for field in required_fields):
                return JsonResponse({'code': 400, 'msg': '缺少必要字段'}, status=400)

            sql = '''
            INSERT INTO admin.commission_an_atricle 
            (func_id, title, work_type, age_classification, introduce, 
             tags, amount_of_money, cover, time, user_id) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''

            filename = f"{self.get_uuid()}.png"
            func_id = self.get_uuid()

            # 图片处理
            re_write_img = ReWriteImg(file=file)
            processed_file = re_write_img.copy_paste()

            # 文件保存路径
            now = datetime.now()
            file_path = os.path.join(BASE_DIR, 'static', 'image', filename)

            # 事务处理
            with transaction.atomic():
                if self.save_file(file_path, processed_file):
                    if self.execute_sql(
                            sql,
                            (
                                    func_id,
                                    data['title'],
                                    data['work_type'],
                                    data['age_classification'],
                                    data['introduce'],
                                    data['tags'],
                                    float(data['amount_of_money']),  # 确保金额为浮点数
                                    filename,
                                    now,
                                    user_id
                            ),
                            return_results=False
                    ):
                        return JsonResponse({'code': 200, 'msg': '添加成功'}, status=200)

            return JsonResponse({'code': 400, 'msg': '添加失败'}, status=400)

        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)