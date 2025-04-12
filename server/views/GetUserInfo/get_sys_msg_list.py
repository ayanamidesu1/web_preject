from base_api import BaseApi
from django.http import JsonResponse

class get_sys_msg_list(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.user.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录'},status=401)
            user_id =str( request.user.id)
            data=self.format_request(request)
            limit=data.get('limit',10)
            offset=data.get('offset',0)
            sql="""select * from messages where (receiver_id='all' or receiver_id=%s) 
            and sender_id='f575b4d3-0683-11ef-adf4-00ffc6b98bdb' and msg_type IN ('all','review_msg','sys_msg')
             order by time desc limit %s offset %s """
            total=self.execute_sql("select count(*) as total from messages where (receiver_id='all' or receiver_id=%s)"
                                   "and sender_id='f575b4d3-0683-11ef-adf4-00ffc6b98bdb'"
                                   " and msg_type IN ('all','review_msg','sys_msg')", (user_id,))[0]['total']
            result=self.execute_sql(sql, (user_id,limit,offset))
            # 标记获取的消息为已读
            if result:
                msg_ids = [str(msg.get('ID')) for msg in result]
                self.execute_sql(
                    "UPDATE messages SET receiver_read_status='已读' "
                    "WHERE id IN %s AND (receiver_id=%s OR receiver_id='all')",
                    (tuple(msg_ids), user_id
                     ))
            # 将结果中的receiver_read_status为已读
            for msg in result:
                if msg.get('receiver_read_status')=='已读':
                    msg['receiver_read_status']='已读'
            return JsonResponse({'code': 200, 'msg': '获取成功', 'data': result, 'total': total},status=200)

        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器内部错误'},status=500)