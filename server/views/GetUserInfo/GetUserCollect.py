from django.db import connection
from django.views import View
from django.http import JsonResponse
from ..log.log import Logger
from datetime import datetime
import json


class GetUserCollect(View):
    logger = Logger()

    def request_path(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR', '未知 IP')
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request_path}'

    def get(self, request):
        self.logger.warning(self.request_path(request) + ' 非法 GET 请求：请求数据为：' + str(request.GET))
        return JsonResponse({'status': 'error', 'message': '非法 GET 请求'}, status=403)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode("utf-8"))
            token = data.get('token')
            userid = data.get('userid')
            middleware_userid=getattr(request, 'userid', None)


            if not token and not userid:
                self.logger.warning(self.request_path(request) + ' token 和 userid 均为空，请求数据为：' + str(data))
                return JsonResponse({'status': 'error', 'message': 'token 和 userid 均为空'}, status=403)

            with connection.cursor() as cursor:

                # 查询收藏列表
                if userid:
                    cursor.execute(
                        'SELECT * FROM user_collection_table WHERE userid=%s AND is_open=%s AND is_collection=%s',
                        [userid, 1, 1])
                else:
                    cursor.execute('SELECT * FROM user_collection_table WHERE userid=%s AND is_collection=%s',
                                   [middleware_userid, 1])

                collect_list = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                rows = [dict(zip(columns, row)) for row in collect_list]

                # 获取作品基本信息
                work_info_dict = {}
                for row in rows:
                    work_id = row.get('workid')
                    work_type = row.get('type')

                    if work_type == 'ill':
                        cursor.execute('SELECT * FROM illustration_work WHERE Illustration_id=%s', [work_id])
                    elif work_type == 'comic':
                        cursor.execute('SELECT * FROM comic WHERE id=%s', [work_id])
                    elif work_type == 'novel':
                        cursor.execute('SELECT * FROM novel_work WHERE work_id=%s', [work_id])
                    else:
                        continue

                    work_details = cursor.fetchone()
                    if work_details:
                        temp_columns = [column[0] for column in cursor.description]
                        work_data = dict(zip(temp_columns, work_details))
                        work_info_dict[work_id] = work_data

                # 获取作者信息
                temp_rows = []
                for row in rows:
                    work_id = row.get('workid')
                    work_type = row.get('type')

                    if work_type == 'ill':
                        cursor.execute('SELECT belong_to_user_id FROM illustration_work WHERE Illustration_id=%s',
                                       [work_id])
                    elif work_type == 'comic':
                        cursor.execute('SELECT belong_to_userid FROM comic WHERE id=%s', [work_id])
                    elif work_type == 'novel':
                        cursor.execute('SELECT belong_to_userid FROM novel_work WHERE work_id=%s', [work_id])
                    else:
                        continue

                    author_id = cursor.fetchone()
                    author_id = author_id[0] if author_id else None
                    if not author_id:
                        row['tips'] = '该作品已被删除或被管理员隐藏或者用户隐藏'
                        row['work_status'] = 'deleted'
                    else:
                        row['tips'] = '作品状态正常'
                        row['work_status'] = 'normal'
                        cursor.execute('SELECT * FROM users WHERE userid=%s', [author_id])
                        userinfo = cursor.fetchone()

                        if userinfo:
                            temp_columns = [column[0] for column in cursor.description]
                            temp_row = dict(zip(temp_columns, userinfo))
                            temp_row.pop('password', None)
                            temp_row.pop('token', None)
                            row['authorinfo'] = temp_row
                        else:
                            row['authorinfo'] = {}
                    row['work_info'] = work_info_dict.get(work_id, {})
                    temp_rows.append(row)
                rows = temp_rows

                return JsonResponse({
                    'status': 'success',
                    'message': '获取收藏列表成功',
                    'data': rows
                })

        except json.JSONDecodeError as e:
            self.logger.error(
                self.request_path(request) + ' JSON 解码错误：请求数据为：' + str(request.body) + ' 错误信息：' + str(e))
            return JsonResponse({'status': 'error', 'message': 'JSON 格式错误'}, status=400)

        except Exception as e:
            self.logger.error(self.request_path(request) + ' 服务器内部错误：' + str(e))
            return JsonResponse({'status': 'error', 'message': '服务器内部错误'}, status=500)
