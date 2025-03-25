from django.db import connection
from django.views import View
from django.http import JsonResponse
from ..log.log import Logger
import json


class GetUserHistoryMsg(View):
    logger = Logger()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'status': 'error', 'message': '请求方式错误'}, status=405)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            msg_type = data['msg_type']
            userid = data['userid']
            friend_id = data['friend_id']
            group_id = data['group_id']

            if not msg_type or not userid:
                self.logger.error('缺少必要参数: {}'.format(data))
                print('缺少必要参数: {}'.format(data))
                return JsonResponse({'status': 'error', 'message': '缺少必要参数'}, status=400)

            if msg_type == 'friend' and friend_id:
                return self._get_messages('friend', userid, data, friend_id=friend_id)
            elif msg_type == 'group' and group_id:
                return self._get_messages('group', userid, data, group_id=group_id)
            else:
                self.logger.error('无效的消息类型或缺少必要参数: {}，请求数据：{}'.format(msg_type,data))
                print('无效的消息类型或缺少必要参数: {}，请求数据{}'.format(msg_type, data))
                return JsonResponse({'status': 'error', 'message': '无效的消息类型或缺少必要参数'}, status=400)

        except json.JSONDecodeError:
            self.logger.error('JSON 解码错误')
            print('JSON 解码错误')
            return JsonResponse({'status': 'error', 'message': 'JSON 解码错误'}, status=400)
        except Exception as e:
            self.logger.error('服务器内部错误: {}'.format(e))
            print('服务器内部错误: {}'.format(e))
            return JsonResponse({'status': 'error', 'message': '服务器内部错误'}, status=500)

    def _get_messages(self, msg_type, userid, data, friend_id=None, group_id=None):
        try:
            with connection.cursor() as cursor:
                if msg_type == 'friend':
                    sql = '''
                        SELECT * FROM messages 
                        WHERE type = %s AND ((sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s))
                        ORDER BY time ASC 
                    '''
                    cursor.execute(sql, ('one_to_one', userid, friend_id, friend_id, userid))
                elif msg_type == 'group':
                    sql = '''
                        SELECT * FROM messages 
                        WHERE type = %s AND group_id = %s 
                        ORDER BY time ASC 
                    '''
                    cursor.execute(sql, ('many_to_many', group_id))

                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                rows = [dict(zip(columns, row)) for row in result]

                if rows:
                    self.logger.info('获取成功, data: {}, 消息内容: {}'.format(data, rows))
                    print('获取成功, data: {}, 消息内容: {}'.format(data, rows))

                    # 成功获取数据后将请求者的消息的读取状态设置为已读
                    if msg_type == 'friend':
                        update_sql = '''
                            UPDATE messages SET receiver_read_status=%s 
                            WHERE type=%s AND ((sender_id=%s AND receiver_id=%s) OR (sender_id=%s AND receiver_id=%s))
                        '''
                        cursor.execute(update_sql, ('已读', 'one_to_one', userid, friend_id, friend_id, userid))
                    elif msg_type == 'group':
                        update_sql = '''
                            UPDATE messages SET receiver_read_status=%s 
                            WHERE type=%s AND group_id=%s AND receiver_id=%s
                        '''
                        cursor.execute(update_sql, ('已读', 'many_to_many', group_id, userid))

                    return JsonResponse({'status': 'success', 'message': '获取成功', 'data': rows}, status=200)
                else:
                    self.logger.info('获取失败, data: {}'.format(data))
                    print('获取失败, data: {}'.format(data))
                    return JsonResponse({'status': 'error', 'message': '获取失败'}, status=400)
        except Exception as e:
            self.logger.error('数据库查询错误: {}'.format(e))
            print('数据库查询错误: {}'.format(e))
            return JsonResponse({'status': 'error', 'message': '数据库查询错误'}, status=500)
