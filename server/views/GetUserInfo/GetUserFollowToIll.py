import json
from django.db import connection
from django.views import View
from django.http import JsonResponse
from ..log.log import Logger


class GetUserFollowToIll(View):
    logger = Logger()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'status': 'success', 'message': 'ok'})

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid = data.get('userid')

            if not userid:
                return JsonResponse({'status': 'error', 'message': 'userid is required'}, status=400)

            with connection.cursor() as cursor:
                # 获取关注列表
                sql = 'SELECT follow_user_id FROM user_follow WHERE user_id=%s'
                cursor.execute(sql, [userid])
                follow_user_ids = [row[0] for row in cursor.fetchall()]

                if not follow_user_ids:
                    self.logger.warning(f'No followers found for user ID: {userid}')
                    return JsonResponse({'status': 'failure', 'message': 'No data found'}, status=400)
                follow_user_ids_tuple = tuple(follow_user_ids)

                # 获取插画信息并按照时间排序
                sql = '''
                    SELECT illustration_work.*, users.user_avatar
                    FROM illustration_work
                    LEFT JOIN users ON illustration_work.belong_to_user_id = users.userid
                    WHERE illustration_work.belong_to_user_id IN %s and work_approved=1 
                    ORDER BY illustration_work.create_time DESC
                '''
                cursor.execute(sql, [tuple(follow_user_ids_tuple)])
                columns = [desc[0] for desc in cursor.description]
                ill_result = cursor.fetchall()
                ill_list = [dict(zip(columns, row)) for row in ill_result]

                self.logger.info(f'Fetched illustrations: {ill_list}')
                return JsonResponse({'status': 'success', 'data': ill_list})

        except json.JSONDecodeError as e:
            self.logger.error(f'JSON decode error: {e}')
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)

        except Exception as e:
            self.logger.error(f'Error occurred: {e}')
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
