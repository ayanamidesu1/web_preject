from django.http import JsonResponse
from base_api import BaseApi

class GetComicList(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if request.user.is_login is False or request.user.role not in ['admin', 'sys_admin']:
                return JsonResponse(
                    {'status': 'error', 'code': 403, 'message': '权限不足', 'msg': '权限不足', 'data': None},
                    status=403)
            data = self.format_request(request)
            limit = data.get('limit', 10)
            offset = data.get('offset', 0)
            sql = '''
            select comic.*,userid,username,user_avatar from comic
            left join users on users.userid=comic.belong_to_userid
             limit %s offset %s
            '''
            total_sql = '''select count(*) total from comic'''
            result = self.execute_sql(sql, (limit, offset), return_results=True)
            total = self.execute_sql(total_sql, return_results=True)[0]['total']
            return JsonResponse({'status': 'success', 'code': 200,
                                 'message': '请求成功', 'msg': '请求成功',
                                 'data': {'work_list': result, 'total': total}}, status=200)
        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse(
                {'status': 'error', 'code': 500, 'message': '服务器错误', 'msg': '服务器错误', 'data': None},
                status=500)


