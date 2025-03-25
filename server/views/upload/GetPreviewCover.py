from django.db import connection
from django.http import JsonResponse
from django.views import View
from datetime import datetime
from ..log.log import Logger
from .CoverHandle import CoverHandle
import json


class GetPreviewCover(View):
    logger = Logger()

    def request_path(self, request):
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR')
        return f'{request_ip} 访问了 {request_path} 接口，时间为 {now}'

    def get(self, request):
        self.logger.warning(self.request_path(request) + ' 请求方式 GET ' + ' 请求数据 ' + str(request.GET))
        return JsonResponse({'status': 'error', 'message': '非法访问'}, status=403)

    def post(self, request, *args, **kwargs):
        try:
            coverhand = CoverHandle()
            data = json.loads(request.body.decode('utf-8'))
            userid=getattr(request,'userid',None)

            title = data.get('title', '实例标题')
            template_name = data.get('template_name', 'template_1')
            if not template_name or template_name == '':
                template_name = 'template_1'
            print(title, template_name)
            temp_cover_path = coverhand.handle(title, None, template_name)

            self.logger.info(
                self.request_path(request) + ' 请求方式 POST ' + ' 请求数据 ' + str(data) + ' 成功信息 ' + str(
                    temp_cover_path))
            return JsonResponse({'status': 'success', 'message': '成功', 'cover_path': temp_cover_path}, status=200)

        except json.JSONDecodeError as e:
            self.logger.error(
                self.request_path(request) + ' 请求方式 POST ' + ' 请求数据 ' + str(request.body) + ' 错误信息 ' + str(
                    e))
            return JsonResponse({'status': 'error', 'message': '请求数据格式错误'}, status=400)
        except Exception as e:
            self.logger.error(
                self.request_path(request) + ' 请求方式 POST ' + ' 请求数据 ' + str(request.body) + ' 错误信息 ' + str(
                    e))
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)
