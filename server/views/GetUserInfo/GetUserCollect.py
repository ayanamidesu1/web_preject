from django.db import connection
from django.views import View
from django.http import JsonResponse
from ..log.log import Logger
from datetime import datetime
import json
from base_api import BaseApi


class GetUserCollect_new(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if self.check_user(request):
                return self.check_user(request)
            user_id = str(request.user.id)
            data = self.format_request(request)
            if data.get('user_id'):
                # 接口复用
                user_id = data.get('user_id')
            limit = int(data.get('limit', 10))
            offset = int(data.get('offset', 0))
            filter_data = data.get('filter_data', {})
            work_type = filter_data.get('work_type', 'all')
            is_open = filter_data.get('is_open', 'all')

            # 构造动态SQL条件
            where_clauses = ["userid = %s"]
            params = [user_id]

            if work_type != 'all':
                where_clauses.append("type = %s")
                params.append(work_type)

            if is_open != 'all':
                if is_open == 'public':
                    where_clauses.append("is_open = '1'")
                elif is_open == 'private':
                    where_clauses.append("is_open = '0'")

            where_clause = " AND ".join(where_clauses)

            # SQL 构建
            sql = f'''
                SELECT *, user_collection_table.workid AS work_id
                FROM user_collection_table
                WHERE {where_clause}
                LIMIT %s OFFSET %s
            '''
            params.extend([limit, offset])

            total_sql = f'''
                SELECT COUNT(*) AS total
                FROM user_collection_table
                WHERE {where_clause}
            '''

            rows = self.execute_sql(sql, params)
            total = self.execute_sql(total_sql, params[:-2])[0]['total']
            # 插画SQL
            ill_sql = '''select illustration_work.*,illustration_work.Illustration_id as work_id ,users.userid as user_id,
            users.username as username,users.user_avatar,illustration_work.name as work_name,u_c.workid as collect_id,
            u_c.is_open as collect_is_open,u_c.is_collection as is_collect,u_c.type as work_type,0 as is_choose
            from illustration_work left join users on users.userid=illustration_work.belong_to_user_id 
            left join user_collection_table as u_c on u_c.workid=illustration_work.Illustration_id
            where illustration_work.Illustration_id=%s'''
            # 漫画SQL
            comic_sql = '''select comic.*, comic.id as work_id,
            users.userid as user_id,
            users.username as username,
            users.user_avatar,
            comic.work_name as work_name,
            u_c.workid as collect_id,
            u_c.is_open as collect_is_open,
            u_c.is_collection as is_collect,u_c.type as work_type,0 as is_choose
            from comic
            left join users on users.userid = comic.belong_to_userid
            left join user_collection_table as u_c on u_c.workid = comic.id
            where comic.id = %s
            '''
            # 小说SQL
            novel_sql = '''select novel_work.*, novel_work.work_id as work_id,
            users.userid as user_id,
            users.username as username,
            users.user_avatar,
            novel_work.work_name as work_name,
            u_c.workid as collect_id,
            u_c.is_open as collect_is_open,
            u_c.is_collection as is_collect,u_c.type as work_type,0 as is_choose
            from novel_work
            left join users on users.userid = novel_work.belong_to_userid
            left join user_collection_table as u_c on u_c.workid = novel_work.work_id
            where novel_work.work_id = %s
            '''
            work_list = {
                'ill': [],
                'comic': [],
                'novel': []
            }
            for i in rows:
                if i['type'] == 'ill':
                    res=self.execute_sql(ill_sql,[i['work_id']])
                    if res:
                        work_list['ill'].append(res[0])
                    else:
                        continue
                if i['type'] == 'comic':
                    res=self.execute_sql(comic_sql, [i['work_id']])
                    if res:
                        work_list['comic'].append(res[0])
                    else:
                        continue
                if i['type'] == 'novel':
                    res=self.execute_sql(novel_sql,[i['work_id']])
                    if res:
                        work_list['novel'].append(res[0])
                    else:
                        continue
            if len(work_list['ill']) > 0 or len(work_list['comic']) > 0 or len(work_list['novel']) > 0:
                return JsonResponse({
                    'code': 200,
                    'msg': '获取成功',
                    'data': {
                        'work_list': work_list,
                        'total': total
                    }
                })
            else:
                return JsonResponse({
                    'code': 200,
                    'msg': '获取成功，但无收藏内容',
                    'data': {
                        'work_list': work_list,
                        'total': total
                    }
                })

        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)


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
            userid=data.get('userid')

            with connection.cursor() as cursor:

                # 查询收藏列表
                if userid:
                    cursor.execute(
                        'SELECT * FROM user_collection_table WHERE userid=%s AND is_open=%s AND is_collection=%s',
                        [userid, 1, 1])

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
