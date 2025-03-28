from base_api import BaseApi
from django.http import JsonResponse
from django.db import connection, transaction, DatabaseError
from log.log import Logger
from datetime import datetime
from .format_html import FormatHtml


class AddComment(BaseApi):
    logger = Logger()
    f_html = FormatHtml()

    def post(self, request, *args, **kwargs):
        try:
            # 验证用户登录状态
            if not request.user.is_login:
                return JsonResponse({'code': 401, 'msg': '用户未登录'}, status=401)

            # 获取并格式化请求数据
            data = self.format_request(request)
            user_id = request.user.id

            # 数据校验
            content = data.get('content', '').strip()
            if not content:
                return JsonResponse({'code': 400, 'msg': '评论内容不能为空'}, status=400)
            content = self.f_html.format_html(content)
            is_main = data.get('is_main', True)
            reply_comment_id = data.get('reply_comment_id')  # 父评论ID
            reply_work_id = data.get('reply_work_id')  # 所属作品ID
            if not reply_work_id:
                return JsonResponse({'code': 400, 'msg': '所属作品ID不能为空'}, status=400)
            reply_work_type = data.get('reply_work_type', 'forum')  # 默认类型为 forum
            reply_user_id = data.get('reply_user_id')  # 回复用户 ID（回复时）

            if not content:
                return JsonResponse({'code': 400, 'msg': '评论内容不能为空'}, status=400)

            # 开启事务
            with transaction.atomic():
                with connection.cursor() as cursor:
                    # 插入评论记录
                    insert_comment_sql = '''
                    INSERT INTO comment 
                    (content, create_time, user_id, is_main, reply_comment_id, reply_work_id, 
                    reply_work_type, reply_user_id) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    '''
                    create_time = datetime.now().isoformat()
                    cursor.execute(
                        insert_comment_sql,
                        [
                            content,
                            create_time,
                            user_id,
                            is_main,
                            reply_comment_id,
                            reply_work_id,
                            reply_work_type,
                            reply_user_id,
                        ],
                    )
                    if cursor.rowcount != 1:
                        raise DatabaseError('评论添加失败')
                    new_comment_id = cursor.execute("SELECT LAST_INSERT_ID()")
                    new_comment_id = cursor.fetchone()[0]
                    now = datetime.now().isoformat()

                # 提交事务并返回成功消息
                return JsonResponse({'code': 200, 'msg': '评论添加成功', "data": {
                    'comment_id': new_comment_id,
                    'create_time': now
                }}, status=200)

        except DatabaseError as e:
            print(e)
            # 数据库事务错误处理
            self.logger.error(f"数据库错误: {e}")
            return JsonResponse({'code': 500, 'msg': '数据库错误'}, status=500)
        except Exception as e:
            # 通用错误处理
            print(e)
            self.logger.error(f"服务器错误: {e}")
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)
