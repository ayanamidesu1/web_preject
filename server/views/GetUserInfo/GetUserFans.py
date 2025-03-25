import json
from django.db import connection
from django.views import View
from django.http import JsonResponse
from ..log.log import Logger


class GetUserFans(View):
    logger = Logger()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'status': 'success', 'message': 'ok'})

    def post(self, request, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                data = json.loads(request.body.decode('utf-8'))
                userid = data['userid']
                if userid:
                    userid = str(userid)
                else:
                    self.logger.warning(data)
                    return JsonResponse({'status': 'failure', 'message': 'No userid found'}, status=400)
                sql = 'select * from user_fans where user_id=%s'
                cursor.execute(sql, [userid])
                columns = [desc[0] for desc in cursor.description]
                result = cursor.fetchall()
                rows = [dict(zip(columns, row)) for row in result]
            if rows:
                self.logger.info(rows)
                return JsonResponse({'status': 'success', 'data': rows})
            else:
                self.logger.warning(data)
                return JsonResponse({'status': 'failure', 'message': 'No data found'}, status=400)
        except Exception as e:

            print(e)
