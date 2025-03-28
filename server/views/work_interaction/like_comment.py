from django.db import connection, transaction, DatabaseError
from django.http import JsonResponse
from datetime import datetime
from base_api import BaseApi


class LikeComment(BaseApi):
    def post(self, request, *args, **kwargs):
        try:
            now = datetime.now()
            # 检查用户是否已登录
            if not request.user.is_login:
                return JsonResponse({
                    'code': 401,
                    'msg': '请先登录'
                }, status=401)
            user_id = request.user.id

            # 获取请求中的评论ID
            data = self.format_request(request)
            comment_id = data.get('comment_id', None)
            if not comment_id:
                return JsonResponse({
                    'code': 400,
                    'msg': '评论id不能为空'
                }, status=400)

            # 使用数据库连接进行查询
            is_like_sql = '''
            select 1 from comment_interaction where comment_id=%s and operate_type='like'
            '''
            result = self.execute_sql(is_like_sql, [comment_id])

            if result:
                # 如果已经点赞，执行取消点赞操作
                del_sql = '''
                delete from comment_interaction where comment_id=%s and operate_type='like' and operate_user_id=%s
                '''
                if self.handle_sql(del_sql, [comment_id, user_id]):
                    return JsonResponse({
                        'code': 200,
                        'msg': '取消点赞成功'
                    }, status=200)
                return JsonResponse({
                    'code': 400,
                    'msg': '取消点赞失败'
                }, status=400)
            else:
                # 如果没有点赞，执行点赞操作
                insert_sql = '''
                insert into comment_interaction (comment_id, operate_user_id, operate_type, datetime) VALUES (%s, %s, %s, %s)
                '''
                if self.handle_sql(insert_sql, [comment_id, user_id, 'like', now]):
                    return JsonResponse({
                        'code': 200,
                        'msg': '点赞成功'
                    }, status=200)
                return JsonResponse({
                    'code': 400,
                    'msg': '点赞失败'
                }, status=400)

        except Exception as e:
            # 使用基类的日志记录方法
            self.error_log(e,request)
            return JsonResponse({
                'code': 500,
                'msg': '服务器错误'
            }, status=500)

    def execute_sql(self, sql, params=None):
        """执行SQL查询并返回结果"""
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql, params or [])
                result = cursor.fetchall()
                return result
            except DatabaseError as e:
                return []

    def handle_sql(self, sql, params=None):
        """执行SQL插入、删除、更新等操作"""
        with transaction.atomic():
            with connection.cursor() as cursor:
                try:
                    cursor.execute(sql, params or [])
                    return True  # 执行成功
                except DatabaseError as e:
                    return False
