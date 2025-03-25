from django.db import connection, transaction
from django.http import JsonResponse
from django.views import View
from ..log.log import Logger
from datetime import datetime
import json


class BaseView(View):
    logger = Logger()

    def get_request_info(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f'{request_ip} at {now} requested {request_path}'


class GetUserFollowList(BaseView):
    def get(self, request):
        self.logger.warning(self.get_request_info(request) + ' GET method not allowed. Params: ' + str(request.GET))
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid = data.get('userid')
            if userid is None:
                userid=getattr(request,'userid',None)
            target_id = data.get('target_id')

            if not userid:
                self.logger.warning(self.get_request_info(request) + ' Missing user ID in request body.')
                return JsonResponse({'status': 'error', 'message': 'Missing user ID'}, status=400)

            with connection.cursor() as cursor:
                sql = 'SELECT * FROM user_follow WHERE user_id=%s AND follow_user_id=%s'
                cursor.execute(sql, [userid, target_id])
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()
                rows = [dict(zip(columns, row)) for row in results]

            self.logger.info(self.get_request_info(request) + ' POST request successful. Params: ' + str(request.body))
            return JsonResponse(
                {'status': 'success', 'message': 'User follow list retrieved successfully', 'data': rows}, status=200)

        except json.JSONDecodeError as e:
            self.logger.error(self.get_request_info(request) + ' JSONDecodeError: ' + str(e))
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
        except Exception as e:
            self.logger.error(self.get_request_info(request) + ' Exception: ' + str(e))
            return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)


class UserAddFollow(BaseView):
    def get(self, request):
        self.logger.warning(self.get_request_info(request) + ' GET method not allowed. Params: ' + str(request.GET))
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid=getattr(request,'userid',None)
            if userid:
                with connection.cursor() as cursor:
                    sql = 'select userid,username from users where userid=%s'
                    cursor.execute(sql, [userid])
                    columns = [desc[0] for desc in cursor.description]
                    results = cursor.fetchall()
                    rows = [dict(zip(columns, row)) for row in results]
                    if rows:
                        userid = rows[0]['userid']
                        username = rows[0]['username']
            else:
                userid = data.get('userid')
                username = data.get('username')
            target_id = data.get('target_id')
            target_username = data.get('target_username')

            if not userid :
                self.logger.warning(self.get_request_info(request) + ' Missing user ID and token in request body.')
                return JsonResponse({'status': 'error', 'message': 'Missing user ID and token'}, status=400)

            with connection.cursor() as cursor:
                sql = 'SELECT * FROM user_follow WHERE user_id=%s AND follow_user_id=%s'
                cursor.execute(sql, [userid, target_id])
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()
                rows = [dict(zip(columns, row)) for row in results]

                if rows:
                    sql = 'DELETE FROM user_follow WHERE user_id=%s AND follow_user_id=%s'
                    cursor.execute(sql, [userid, target_id])
                    transaction.commit()
                    self.logger.info(
                        self.get_request_info(request) + '取消关注成功： POST request successful. Params: ' + str(
                            request.body))
                    return JsonResponse({'status': 'success', 'message': '取消关注成功'}, status=200)

                sql = (
                    'INSERT INTO user_follow (username, user_id, follow_username, follow_user_id, follow_time, status) '
                    'VALUES (%s, %s, %s, %s, %s, %s)')
                cursor.execute(sql, [username, userid, target_username, target_id, datetime.now(), 1])
                transaction.commit()
                self.logger.info(
                    self.get_request_info(request) + ' 关注成功：POST request successful. Params: ' + str(request.body))
                return JsonResponse({'status': 'success', 'message': '关注成功'}, status=200)

        except json.JSONDecodeError as e:
            self.logger.error(self.get_request_info(request) + ' JSONDecodeError: ' + str(e))
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
        except Exception as e:
            self.logger.error(self.get_request_info(request) + ' Exception: ' + str(e))
            return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)
