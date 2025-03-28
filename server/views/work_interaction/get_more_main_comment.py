from base_api import BaseApi
from django.http import JsonResponse
from djangoProject.log.log import Logger


class GetMoreMainComment(BaseApi):
    logger = Logger()

    def post(self, request, *args, **kwargs):
        try:
            # 获取并格式化请求数据
            data = self.format_request(request)
            work_id = data.get('work_id')
            work_type = data.get('work_type')
            limit = data.get('limit', 10)
            offset = data.get('offset', 0)
            reply_limit = data.get('reply_limit', 3)
            reply_offset = data.get('reply_offset', 0)

            try:
                user_id = request.user.id
            except Exception:
                user_id = None

            # 参数校验
            if not work_id or not work_type:
                return JsonResponse({'code': 400, 'msg': '缺少必要的参数'}, status=400)

            # 主评论查询 SQL，包含点赞状态
            main_comment_sql = '''
                SELECT 
                    comment.id AS comment_id,
                    comment.content AS content,
                    comment.create_time AS create_time,
                    comment.user_id AS user_id,
                    comment.is_main AS is_main,
                    comment.reply_comment_id AS reply_comment_id,
                    comment.reply_work_id AS reply_work_id,
                    comment.reply_work_type AS reply_work_type,
                    COALESCE(like_count_table.like_count, 0) AS like_count,
                    user_table.username AS username,
                    user_table.avatar AS avatar,
                    EXISTS(
                        SELECT 1 FROM comment_interaction 
                        WHERE comment_interaction.comment_id = comment.id 
                        AND comment_interaction.operate_user_id = %s 
                        AND comment_interaction.operate_type = 'like'
                    ) AS is_like
                FROM comment
                LEFT JOIN (
                    SELECT 
                        comment_interaction.comment_id AS comment_id,
                        COUNT(*) AS like_count
                    FROM comment_interaction
                    WHERE comment_interaction.operate_type = 'like'
                    GROUP BY comment_interaction.comment_id
                ) AS like_count_table ON comment.id = like_count_table.comment_id
                LEFT JOIN users AS user_table ON comment.user_id = user_table.user_id
                WHERE comment.is_main = '1' AND comment.reply_work_id = %s AND comment.reply_work_type = %s
                order by comment.create_time
                LIMIT %s OFFSET %s;
            '''

            # 子评论查询 SQL
            reply_comment_sql = '''
                SELECT 
                    reply.id AS comment_id,
                    reply.content AS content,
                    reply.create_time AS create_time,
                    reply.user_id AS user_id,
                    reply.is_main AS is_main,
                    reply.reply_comment_id AS reply_comment_id,
                    reply.reply_work_id AS reply_work_id,
                    reply.reply_work_type AS reply_work_type,
                    COALESCE(like_count_table.like_count, 0) AS like_count,
                    user_table.username AS username,
                    user_table.avatar AS avatar,
                    reply_target_user_table.username AS reply_username,
                    reply_target_user_table.avatar AS reply_avatar,
                    reply_target_user_table.user_id AS reply_user_id,
                    EXISTS(
                        SELECT 1 FROM comment_interaction 
                        WHERE comment_interaction.comment_id = reply.id 
                        AND comment_interaction.operate_user_id = %s 
                        AND comment_interaction.operate_type = 'like'
                    ) AS is_like
                FROM comment AS reply
                LEFT JOIN (
                    SELECT 
                        comment_interaction.comment_id AS comment_id,
                        COUNT(*) AS like_count
                    FROM comment_interaction
                    WHERE comment_interaction.operate_type = 'like'
                    GROUP BY comment_interaction.comment_id
                ) AS like_count_table ON reply.id = like_count_table.comment_id
                LEFT JOIN users AS user_table ON reply.user_id = user_table.user_id
                LEFT JOIN users AS reply_target_user_table ON reply.reply_user_id = reply_target_user_table.user_id
                WHERE reply.is_main = '0' AND reply.reply_comment_id = %s order by reply.create_time
                LIMIT %s OFFSET %s;
            '''

            # 查询主评论
            main_comments = self.execute_sql(main_comment_sql, [user_id, work_id, work_type, limit, offset])

            # 查询并附加子评论
            for comment in main_comments:
                comment_id = comment['comment_id']
                reply_comments = self.execute_sql(reply_comment_sql, [user_id, comment_id, reply_limit, reply_offset])

                # 格式化子评论数据
                comment['reply_list'] = [
                    {
                        'comment_id': reply.get('comment_id'),
                        'content': reply.get('content', ''),
                        'create_time': reply.get('create_time', ''),
                        'is_main': reply.get('is_main', '0'),
                        'user': {
                            'username': reply.get('username', ''),
                            'avatar': reply.get('avatar', ''),
                            'user_id': reply.get('user_id', None)
                        },
                        'reply_user': {
                            'username': reply.get('reply_username', ''),
                            'avatar': reply.get('reply_avatar', ''),
                            'user_id': reply.get('reply_user_id', None)
                        },
                        'like_count': reply.get('like_count', 0),
                        'is_like': reply.get('is_like', False)
                    }
                    for reply in reply_comments
                ]

                # 格式化主评论用户数据
                comment['user'] = {
                    'username': comment.pop('username', ''),
                    'avatar': comment.pop('avatar', ''),
                    'user_id': comment.pop('user_id', None)
                }

            # 返回结果
            return JsonResponse({
                'code': 200,
                'msg': '获取成功',
                'data': main_comments
            })

        except Exception as e:
            self.logger.error(f'Error in GetMoreMainComment: {e}')
            return JsonResponse({'code': 500, 'msg': '服务器内部错误'}, status=500)
