from django.shortcuts import render
from django.views import View
from .models.comic_recommend import ComicRecommendation
from .models.ill_recommend import IllRecommendation
from .models.novel_recommend import NovelRecommendation
from ..log.log import Logger
from datetime import datetime
import json
from django.db import connection
from django.http import JsonResponse


class recommend(View):
    logger = Logger()
    ill_recommend = IllRecommendation()
    comic_recommend = ComicRecommendation()
    novel_recommend = NovelRecommendation()

    def request_path(self, request):
        request_path = request.path
        request_ip = request.META['REMOTE_ADDR']
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        return f'{request_ip}在{now}访问了{request_path}'

    def get(self, request):
        self.logger.warning(self.request_path(request) + '非法GET访问：请求数据为：' + str(request.GET))
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid=getattr(request, 'userid',None)
            token = data.get('token')
            work_type = data.get('work_type')
            work_offset = data.get('work_offset')
            work_limit = data.get('work_limit')
            admin_userid = 'f575b4d3-0683-11ef-adf4-00ffc6b98bdb'
            if not userid:
                if not token:
                    print('token为空')
                    self.logger.warning(self.request_path(request) + 'token为空')
                    return JsonResponse({'status': 'error', 'message': 'token为空'}, status=400)

                with connection.cursor() as cursor:
                    if token == 'sunyuanling':
                        cursor.execute('SELECT token FROM users WHERE userid=%s', [admin_userid])
                        result = cursor.fetchone()
                        if result:
                            token = result[0]
                        else:
                            return JsonResponse({'status': 'error', 'message': '未找到管理员用户'}, status=400)

                    cursor.execute('SELECT userid FROM users WHERE token=%s', [token])
                    result = cursor.fetchone()
                    if result:
                        userid = result[0]
                    else:
                        print('用户不存在')
                        self.logger.warning(self.request_path(request) + '用户不存在')
                        return JsonResponse({'status': 'error', 'message': '用户不存在'}, status=400)

            if work_type == 'ill':
                work_info_list = self.ill_recommend.get_userid(userid, work_offset, work_limit)
                return JsonResponse({'status': 'success', 'data': work_info_list}, status=200)
            if work_type == 'comic':
                work_info_list = self.comic_recommend.get_userid(userid, work_offset, work_limit)
                return JsonResponse({'status': 'success', 'data': work_info_list}, status=200)
            if work_type == 'novel':
                work_info_list = self.novel_recommend.get_userid(userid, work_offset, work_limit)
                return JsonResponse({'status': 'success', 'data': work_info_list}, status=200)

        except json.JSONDecodeError as e:
            print(e)
            self.logger.error(self.request_path(request) + '请求数据格式错误：' + str(e))
            return JsonResponse({'status': 'error', 'message': '请求数据格式错误'}, status=400)
        except Exception as e:
            print(e)
            self.logger.error(self.request_path(request) + '服务器错误：' + str(e))
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)
