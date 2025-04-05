import os.path
from datetime import datetime

from base_api import BaseApi
from django.http import JsonResponse
from format_img import ReWriteImg
from djangoWebServer.settings import BASE_DIR


class AddFunc(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录'}, status=401)
            user_id = request.user.id
            file = request.FILES.get('file')
            data = request.POST.get('data')
            if not file:
                return JsonResponse({'code': 400, 'msg': '文件为空'}, status=400)
            if not data:
                return JsonResponse({'code': 400, 'msg': '数据为空'}, status=400)
            sql = '''
            insert into commission_an_atricle (func_id, title, work_type, age_classification, introduce, tags,
             amount_of_money, cover, time, user_id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            filename = str(self.get_uuid()) + '.png'
            func_id = self.get_uuid()
            re_write_img = ReWriteImg(file=file)
            file = re_write_img.copy_paste()
            now = datetime.now()
            file_path = os.path.join(BASE_DIR, 'static', 'image', filename)
            if self.save_file(file_path, file):
                if self.execute_sql(sql,
                                    (func_id, data.get('title'), data.get('work_type'), data.get('age_classification'),
                                     data.get('introduce'), data.get('tags'), data.get('amount_of_money'),
                                     filename, now, user_id), return_results=False):
                    return JsonResponse({'code': 200, 'msg': '添加成功'}, status=200)
                return JsonResponse({'code': 400, 'msg': '添加失败，插入数据失败'}, status=400)
            return JsonResponse({'code': 400, 'msg': '添加失败，保存文件失败'}, status=400)


        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)
