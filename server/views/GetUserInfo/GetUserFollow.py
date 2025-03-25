from django.db import connection
from django.http import JsonResponse
from django.views import View
import json
from ..log.log import Logger


class GetUserFollow(View):
    logger = Logger()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'status': 'success', 'message': 'ok'})

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            token = data.get('token')
            userid = getattr(request, 'userid', None)
            if not userid:
                if token:
                    with connection.cursor() as cursor:
                        sql = 'SELECT userid FROM users WHERE token=%s'
                        cursor.execute(sql, [token])
                        result = cursor.fetchone()
                        if result:
                            userid = result[0]
                        else:
                            # Handle case where token is not found
                            return JsonResponse({'status': 'failure', 'message': 'Invalid token'}, status=400)

                # If token is not provided, fallback to userid from the request
                if userid is None:
                    userid = data.get('userid')
                    if not userid:
                        return JsonResponse({'status': 'failure', 'message': 'User ID is required'}, status=400)

            with connection.cursor() as cursor:
                sql = 'SELECT * FROM user_follow WHERE user_id=%s'
                cursor.execute(sql, [userid])
                columns = [desc[0] for desc in cursor.description]
                result = cursor.fetchall()
                rows = [dict(zip(columns, row)) for row in result]

            if rows:
                self.logger.info(f'User follow data: {rows}')
                return JsonResponse({'status': 'success', 'data': rows})
            else:
                self.logger.warning(f'No data found for user: {userid}')
                return JsonResponse({'status': 'failure', 'message': 'No data found'}, status=404)

        except json.JSONDecodeError as e:
            self.logger.error(f'JSON decode error: {e}')
            return JsonResponse({'status': 'fail', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            self.logger.error(f'An unexpected error occurred: {e}')
            return JsonResponse({'status': 'fail', 'message': 'Internal server error'}, status=500)
