from base_api import BaseApi
from django.http import JsonResponse


class GetMsgList(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.user.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录'}, status=401)

            data = self.format_request(request)
            target_id = data.get('target_id')
            if not target_id:
                return JsonResponse({'code': 400, 'msg': '缺少参数'}, status=400)

            limit = int(data.get('limit', 20))  # 限制返回条数
            offset = int(data.get('offset', 0))  # 偏移量

            sql = '''
            SELECT * FROM messages 
            WHERE ((sender_id = %s AND receiver_id = %s) 
               OR (sender_id = %s AND receiver_id = %s)) 
               AND type = 'one_to_one' 
            ORDER BY id DESC  -- 倒序获取最新消息
            LIMIT %s OFFSET %s
            '''
            result = self.execute_sql(sql, (request.user.id, target_id, target_id, request.user.id, limit, offset))
            get_total_sql='''
            select count(*) as total from messages where (sender_id = %s AND receiver_id = %s) 
               OR (sender_id = %s AND receiver_id = %s) 
               AND type = 'one_to_one' 
            '''
            #更新消息为已读
            update_sql='''
            update messages set receiver_read_status='已读' where sender_id=%s and receiver_id=%s 
            '''
            self.execute_sql(update_sql,(request.user.id, target_id))
            total=self.execute_sql(get_total_sql,(request.user.id, target_id, target_id, request.user.id))[0]['total']
            return JsonResponse({'code': 200, 'msg': '获取成功', 'data': result if result else [],'total':total}
                                , status=200)

        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)
