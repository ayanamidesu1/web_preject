from django.http import JsonResponse
from base_api import BaseApi

class ResetPassword(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            data=self.format_request(request)
            username=data.get('username')
            password=data.get('password')
            phone=data.get('phone')
            email=data.get('email')
            if username and password and phone and email:
                sql='''
                select * from users where phone=%s and email=%s
                '''
                if self.execute_sql(sql, (phone, email)):
                    sql='''
                    update users set password=%s where username=%s and phone=%s and email=%s
                    '''
                    if self.execute_sql(sql, (password, username, phone, email)):
                        return JsonResponse({'code': 200, 'msg': '密码重置成功'}, status=200)
                    else:
                        return JsonResponse({'code': 400, 'msg': '密码重置失败'}, status=400)
                return JsonResponse({'code': 400, 'msg': '用户名或手机号或邮箱错误'}, status=400)
            return JsonResponse({'code': 400, 'msg': '参数错误'}, status=400)
        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'},status=500)