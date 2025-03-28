from base_api import BaseApi
from django.http import  JsonResponse

class AddMsg(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:

        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'},status=500)