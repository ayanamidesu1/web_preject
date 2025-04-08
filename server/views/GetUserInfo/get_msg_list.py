import json
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

            limit = int(data.get('limit', 20))
            offset = int(data.get('offset', 0))

            # 查询消息列表
            sql = '''
            SELECT * FROM messages 
            WHERE ((sender_id = %s AND receiver_id = %s) 
               OR (sender_id = %s AND receiver_id = %s)) 
               AND type = 'one_to_one' 
            ORDER BY id DESC
            LIMIT %s OFFSET %s
            '''
            messages = self.execute_sql(sql, (request.user.id, target_id, target_id, request.user.id, limit, offset))

            # 仅格式化 type='review_msg' 的 content 字段
            formatted_messages = []
            for msg in messages:
                content = msg.get('content', '')
                message_type = msg.get('type', '')  # 注意这里是 type 字段，不是 msg_type

                # 仅处理 type='review_msg' 的消息
                if message_type == 'review_msg':
                    try:
                        # 确保 content 是字符串时才尝试解析
                        if isinstance(content, str):
                            parsed_content = json.loads(content)
                            if not isinstance(parsed_content, dict):
                                parsed_content = {'error': 'Content must be a JSON dict'}
                        else:
                            parsed_content = {'error': 'Content is not a string'}

                        # 验证 type 字段
                        if parsed_content.get('type') != 'review_msg':
                            parsed_content['type'] = 'review_msg'  # 自动修复

                        content = parsed_content
                    except json.JSONDecodeError:
                        content = {'error': 'Invalid JSON format'}

                # 其他类型的消息（如 type='notice'）保持 content 原样
                formatted_msg = {**msg, 'content': content}
                formatted_messages.append(formatted_msg)

            # 更新消息为已读（注意参数顺序）
            update_sql = '''
            UPDATE messages SET receiver_read_status = '已读' 
            WHERE sender_id = %s AND receiver_id = %s 
            '''
            self.execute_sql(update_sql, (target_id, request.user.id))

            # 获取消息总数
            get_total_sql = '''
            SELECT COUNT(*) AS total FROM messages 
            WHERE ((sender_id = %s AND receiver_id = %s) 
               OR (sender_id = %s AND receiver_id = %s)) 
               AND type = 'one_to_one'
            '''
            total = self.execute_sql(get_total_sql, (request.user.id, target_id, target_id, request.user.id))[0][
                'total']

            return JsonResponse({
                'code': 200,
                'msg': '获取成功',
                'data': formatted_messages,
                'total': total
            }, status=200)

        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)