from base_api import BaseApi
from django.http import JsonResponse

class GetUserInfoById(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            data=self.format_request(request)
            user_id=data.get('user_id')
            if not user_id:
                return JsonResponse({'status': 'error', 'message': '缺少参数user_id','code':400},status=400)
            sql='''
            select username,userid,user_avatar,user_back_img,select_work,user_self_introduction
             from users where userid=%s and (account_status='1' or account_status=1)
            '''
            result=self.execute_sql(sql, (user_id,))
            if result:
                user_info=result[0]
                return JsonResponse({'status': 'success', 'message': '获取用户信息成功','code':200,'data':user_info},status=200)
            else:
                return JsonResponse({'status': 'error', 'message': '用户不存在','code':400},status=400)
        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'status': 'error', 'message': '获取用户信息失败','code':500},status=500)