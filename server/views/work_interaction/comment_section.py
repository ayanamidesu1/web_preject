from django.db import connection
from django.views import View
from django.http import JsonResponse
from datetime import datetime
import json
from ..log.log import Logger


class AddCommentSection(View):
    logger = Logger()

    def request_path(self, request):
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR')
        return f'{request_ip}访问了{request_path}接口，时间为{now}'

    def get(self, request):
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.logger.warning(self.request_path(request) + '请求数据为：' + str(request.GET))
        return JsonResponse({'status': 'error', 'message': '非法GET请求'}, status=403)

    def post(self, request, *args, **kwargs):
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        try:
            data = json.loads(request.body.decode('utf-8'))
            token = data.get('token')
            user_id=getattr(request,'userid',None)
            key = data.get('key')
            admin_userid = 'f575b4d3-0683-11ef-adf4-00ffc6b98bdb'
            if not user_id:
                if token == 'sunyuanling' or key == 'sunyuanling':
                    # 使用管理员信息进行插入操作
                    user_id = admin_userid
                else:
                    with connection.cursor() as cursor:
                        cursor.execute('SELECT userid FROM users WHERE token=%s', [token])
                        result = cursor.fetchone()
                        if not result:
                            self.logger.warning(self.request_path(request) + '请求数据为：' + str(
                                request.POST) + '，错误信息为：' + 'token无效')
                            return JsonResponse({'status': 'error', 'message': 'token无效'}, status=400)
                        user_id = result[0]
            main_user_id = data.get('main_user_id')
            is_root_comment = data.get('is_root_comment')
            if is_root_comment == '1' or is_root_comment == True or is_root_comment == 1:
                main_user_id = user_id
            else:
                main_user_id = data.get('main_user_id')
            content = data.get('content')
            if not content:
                self.logger.warning(
                    self.request_path(request) + '请求数据为：' + str(request.POST) + '，错误信息为：' + 'content缺失')
                return JsonResponse({'status': 'error', 'message': '评论内容不能为空'}, status=400)

            sql = ('INSERT INTO comment (work_id, work_type, is_root_comment, send_userid, content, date, '
                   'main_userid, main_comment_id, reply_comment_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
            with connection.cursor() as cursor:
                cursor.execute(sql, [data.get('work_id'), data.get('work_type'), data.get('is_root_comment'),
                                     user_id, content, now, main_user_id,
                                     int(data.get('main_comment_id')), int(data.get('reply_comment_id'))])

            return JsonResponse({'status': 'success', 'message': '评论成功'}, status=200)

        except json.JSONDecodeError as e:
            print(e)
            self.logger.error(self.request_path(request) + '请求数据为：' + str(request.POST) + '，错误信息为：' + str(e))
            return JsonResponse({'status': 'error', 'message': '请求数据格式错误'}, status=400)
        except Exception as e:
            print(e)
            self.logger.error(self.request_path(request) + '请求数据为：' + str(request.POST) + '，错误信息为：' + str(e))
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)


class LikeComment(View):
    logger = Logger()

    DATE_FORMATS = [
        "%Y年%m月%d日%H:%M:%S",  # e.g., 2024年5月8日00:30:25
        "%Y-%m-%d %H:%M:%S",  # e.g., 2024-05-08 01:09:09
        "%Y-%m-%dT%H:%M:%S"  # e.g., 2024-05-08T01:09:09
    ]

    def request_path(self, request):
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR')
        return f'{request_ip}访问了{request_path}接口，时间为{now}'

    def parse_date(self, date_str):
        for fmt in self.DATE_FORMATS:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unsupported date format: {date_str}")

    def get(self, request):
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.logger.warning(self.request_path(request) + '请求数据为：' + str(request.GET))
        return JsonResponse({'status': 'error', 'message': '非法GET请求'}, status=403)

    def post(self, request, *args, **kwargs):
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            operate = data.get('operate')
            token = data.get('token')
            userid=getattr(request,'userid',None)
            print(token)
            admin_userid = 'f575b4d3-0683-11ef-adf4-00ffc6b98bdb'
            if not userid:
                if token:
                    print('token错误')
                    self.logger.error(
                        self.request_path(request) + '请求数据为：' + str(request.POST) + '，错误信息为：' + '没有token')
                    return JsonResponse({'status': 'error', 'message': '没有token'}, status=400)
                if token == 'sunyuanling':
                    userid = admin_userid
                with connection.cursor() as cursor:
                    cursor.execute('select userid,username from users where token=%s or userid=%s', [token,admin_userid])
                    result = cursor.fetchone()
                    if result:
                        userid = result[0]
                        username = result[1]
                    else:
                        print('admin info error and user info error')
                        self.logger.error(
                            self.request_path(request) + '请求数据为：' + str(request.POST) + '，错误信息为：' + 'token错误')
                        return JsonResponse({'status': 'error', 'message': 'token错误'}, status=400)
            with connection.cursor() as cursor:
                if operate == 'like':
                    try:
                        comment_id = data.get('comment_id')
                        work_type = data.get('work_type')
                        work_id = data.get('work_id')
                        if not comment_id:
                            print('没有comment_id')
                            self.logger.error(self.request_path(request) + '请求数据为：' + str(
                                request.POST) + '，错误信息为：' + '没有comment_id')
                            return JsonResponse({'status': 'error', 'message': '没有comment_id'}, status=400)
                        cursor.execute(
                            'select * from comment_like where comment_id=%s and userid=%s and work_type=%s and work_id=%s',
                            [comment_id, userid, work_type, work_id])
                        result = cursor.fetchone()
                        if result:
                            cursor.execute(
                                'delete from comment_like where comment_id=%s and userid=%s and work_type=%s and work_id=%s',
                                [comment_id, userid, work_type, work_id])
                            return JsonResponse({'status': 'success', 'message': '取消点赞成功'}, status=200)
                        else:
                            cursor.execute('insert into comment_like(comment_id,userid,work_type,time,work_id) values(%s,%s,'
                                           '%s,%s,%s)',
                                           [comment_id, userid, work_type, now,work_id])
                            if cursor.rowcount == 1:
                                return JsonResponse({'status': 'success', 'message': '点赞成功'}, status=200)
                            else:
                                print('点赞失败')
                                return JsonResponse({'status': 'error', 'message': '点赞失败'}, status=400)
                    except Exception as e:
                        print(e)
                        self.logger.error(self.request_path(request) + '请求数据为：' + str(request.POST) + '，错误信息为：' + str(e))
                        return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)
                if operate == 'search':
                    comment_id = data.get('comment_id')
                    work_type = data.get('work_type')
                    if not comment_id:
                        self.logger.error(self.request_path(request) + '请求数据为：' + str(
                            request.POST) + '，错误信息为：' + '没有comment_id')
                        return JsonResponse({'status': 'error', 'message': '没有comment_id'}, status=400)
                    cursor.execute('select * from comment_like where comment_id=%s and userid=%s and work_type=%s',
                                   [comment_id, userid, work_type])
                    result = cursor.fetchone()
                    if result:
                        return JsonResponse({'status': 'success', 'message': '查询成功', 'is_like': True}, status=200)
                    else:
                        return JsonResponse({'status': 'success', 'message': '查询成功', 'is_like': False}, status=200)
                if operate == 'search_all':
                    work_type = data.get('work_type')
                    comment_id = data.get('comment_id')
                    if not comment_id:
                        self.logger.error(self.request_path(request) + '请求数据为：' + str(
                            request.POST) + '，错误信息为：' + '没有comment_id')
                        return JsonResponse({'status': 'error', 'message': '没有comment_id'}, status=400)
                    cursor.execute('select count(*) from comment_like where work_type=%s and comment_id=%s',
                                   [work_type, comment_id])
                    result = cursor.fetchone()
                    if result:
                        return JsonResponse({'status': 'success', 'message': '查询成功', 'count': result[0]},
                                            status=200)
                    else:
                        return JsonResponse({'status': 'error', 'message': '查询失败'}, status=400)
                return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)

        except Exception as e:
            print(e)
            self.logger.error(self.request_path(request) + '请求数据为：' + str(request.POST) + '，错误信息为：' + str(e))
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)


class GetCommentSection(View):
    logger = Logger()

    DATE_FORMATS = [
        "%Y年%m月%d日%H:%M:%S",  # e.g., 2024年5月8日00:30:25
        "%Y-%m-%d %H:%M:%S",  # e.g., 2024-05-08 01:09:09
        "%Y-%m-%dT%H:%M:%S"  # e.g., 2024-05-08T01:09:09
    ]

    def request_path(self, request):
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR')
        return f'{request_ip}访问了{request_path}接口，时间为{now}'

    def parse_date(self, date_str):
        for fmt in self.DATE_FORMATS:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unsupported date format: {date_str}")

    def search_like(self, comment_id, work_id, work_type, userid, cursor):
        cursor.execute('select * from comment_like where comment_id=%s and userid=%s and work_type=%s and work_id=%s',
                       [comment_id, userid, work_type, work_id])
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False

    def search_all(self, comment_id, work_id, work_type, cursor):
        cursor.execute('select count(*) from comment_like where work_type=%s and comment_id=%s and work_id=%s',
                       [work_type, comment_id, work_id])
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return 0

    def get(self, request):
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.logger.warning(self.request_path(request) + '请求数据为：' + str(request.GET))
        return JsonResponse({'status': 'error', 'message': '非法GET请求'}, status=403)

    def post(self, request, *args, **kwargs):
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        try:
            data = json.loads(request.body.decode('utf-8'))
            token = data.get('token')
            user_id=getattr(request, 'userid', None)
            key = data.get('key')
            work_id = data.get('work_id')
            work_type = data.get('work_type')
            admin_userid = 'f575b4d3-0683-11ef-adf4-00ffc6b98bdb'
            limit = int(data.get('limit', 10))
            offset = int(data.get('offset', 0))
            if not user_id:
                if token == 'sunyuanling' or key == 'sunyuanling':
                    user_id = admin_userid
                else:
                    with connection.cursor() as cursor:
                        cursor.execute('SELECT userid FROM users WHERE token=%s', [token])
                        result = cursor.fetchone()
                        if not result:
                            self.logger.warning(self.request_path(request) + '请求数据为：' + str(
                                request.POST) + '，错误信息为：' + 'token无效')
                            return JsonResponse({'status': 'error', 'message': 'token无效'}, status=400)
                        user_id = result[0]

            if not work_id:
                self.logger.warning(
                    self.request_path(request) + '请求数据为：' + str(request.POST) + '，错误信息为：' + 'work_id缺失')
                return JsonResponse({'status': 'success', 'message': 'work_id缺失', 'data': '登录后查看所有评论'},
                                    status=200)

            with connection.cursor() as cursor:
                # 获取总评论数
                cursor.execute('SELECT COUNT(*) FROM comment WHERE work_id=%s AND work_type=%s', [work_id, work_type])
                total_comments = cursor.fetchone()[0]

                # 获取分页数据（包括主评论）
                cursor.execute('''
                    SELECT * FROM comment
                    WHERE work_id=%s AND work_type=%s
                    ORDER BY date DESC
                    LIMIT %s OFFSET %s
                ''', [work_id, work_type, limit, offset])
                result = cursor.fetchall()

                if not result:
                    self.logger.warning(
                        self.request_path(request) + '请求数据为：' + str(request.POST) + '，错误信息为：' + '该作品没有评论')
                    return JsonResponse({'status': 'success', 'message': '该作品没有评论'}, status=202)

                columns = [column[0] for column in cursor.description]
                rows = [dict(zip(columns, row)) for row in result]

                # 获取所有用户信息
                user_ids = set(row['send_userid'] for row in rows)
                cursor.execute('SELECT userid, username, user_avatar FROM users WHERE userid IN %s', [tuple(user_ids)])
                user_info = {userid: (username, user_avatar) for userid, username, user_avatar in cursor.fetchall()}

                # 获取所有子评论
                parent_comment_ids = [row['comment_id'] for row in rows if
                                      row['is_root_comment'] in ['否', '0', False, 0]]
                if parent_comment_ids:
                    cursor.execute('''
                        SELECT * FROM comment
                        WHERE comment_id IN %s
                        ORDER BY date DESC
                    ''', [tuple(parent_comment_ids)])
                    child_comments = cursor.fetchall()

                    child_columns = [column[0] for column in cursor.description]
                    child_rows = [dict(zip(child_columns, row)) for row in child_comments]

                    # 将子评论按主评论 ID 组织起来
                    child_comments_by_parent = {}
                    for child in child_rows:
                        parent_id = child['main_comment_id']
                        if parent_id not in child_comments_by_parent:
                            child_comments_by_parent[parent_id] = []
                        child_comments_by_parent[parent_id].append(child)

                else:
                    child_comments_by_parent = {}

                data = []
                # 处理每一条评论数据
                for row in rows:
                    if row['is_root_comment'] in ['是', True, 1, '1']:
                        # 确保 'date' 是 datetime 对象
                        if isinstance(row['date'], str):
                            try:
                                row['date'] = self.parse_date(row['date'])
                            except ValueError as e:
                                self.logger.warning(self.request_path(request) + '请求数据为：' + str(
                                    request.POST) + '，错误信息为：' + str(e))
                                row['date'] = datetime.now()  # 备用值或处理错误

                        row['time'] = row['date'].strftime("%Y年%m月%d日 %H时%M分%S秒")
                        row['is_main'] = row['is_root_comment'] in ['是', True, 1]
                        row['userid'] = row['send_userid']
                        user_data = user_info.get(row['send_userid'], ('未知', 'work_like'))
                        row['username'], row['user_avatar'] = user_data
                        row['msg_content'] = row['content']
                        row['is_replay'] = row['main_userid'] != row['send_userid']
                        row['comment_id'] = row['comment_id']
                        row['main_comment_id'] = row['main_comment_id'],
                        row['user_is_like_comment']=self.search_like(row['comment_id'],work_id,work_type,user_id,cursor),
                        row['like_comment_count']=self.search_all(row['comment_id'],work_id,work_type,cursor)
                        # 添加子评论
                        row['replies'] = [dict(
                            comment_id=child['comment_id'],
                            userid=child['send_userid'],
                            username=user_info.get(child['send_userid'], ('未知', 'work_like'))[0],
                            user_avatar=user_info.get(child['send_userid'], ('未知', 'work_like'))[1],
                            msg_content=child['content'],
                            time=self.parse_date(child['date']).strftime("%Y年%m月%d日 %H时%M分%S秒"),
                            is_main=False,
                            is_replay=child['main_userid'] != child['send_userid'],
                            main_comment_id=child['main_comment_id'],
                            reply_comment_id=child['reply_comment_id'],
                            user_is_like_comment=self.search_like(child['comment_id'],work_id,work_type,user_id,cursor),
                            like_comment_count=self.search_all(child['comment_id'],work_id,work_type,cursor)
                        ) for child in child_comments_by_parent.get(row['comment_id'], [])]
                        #查找回复的谁，用户名
                        for reply in row['replies']:
                            if reply['reply_comment_id']:
                                cursor.execute('''
                                            SELECT
                                                u.username AS reply_username
                                            FROM
                                                comment c
                                            JOIN
                                                users u ON c.send_userid = u.userid
                                            WHERE
                                                c.comment_id = %s
                                        ''', [reply['reply_comment_id']])

                                result = cursor.fetchone()
                                if result:
                                    reply['reply_username'] = result[0]
                                else:
                                    reply['reply_username'] = '未知'
                        data.append(row)

                return JsonResponse({
                    'status': 'success',
                    'message': '查询成功',
                    'data': data,
                    'total_comments': total_comments
                })

        except json.JSONDecodeError as e:
            self.logger.error(self.request_path(request) + '请求数据为：' + str(request.POST) + '，错误信息为：' + str(e))
            return JsonResponse({'status': 'error', 'message': '请求数据格式错误'}, status=400)
        except Exception as e:
            self.logger.error(self.request_path(request) + '请求数据为：' + str(request.POST) + '，错误信息为：' + str(e))
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)
