from django.http import JsonResponse
from base_api import BaseApi
from log.log import Logger


class GetCommentList(BaseApi):
    logger = Logger()

    def post(self, request, *args, **kwargs):
        try:
            # 获取并格式化请求数据
            request_data = self.format_request(request)
            print(request_data)
            limit = request_data.get('limit', 3)
            offset = request_data.get('offset', 0)
            work_id = request_data.get('work_id', '')
            work_type = request_data.get('work_type', '')
            reply_limit = request_data.get('reply_limit', 3)
            reply_offset = request_data.get('reply_offset', 0)
            try:
                user_id = request.user.id
            except Exception as e:
                user_id = None

            if not work_id or not work_type:
                return JsonResponse({'code': 400, 'msg': '缺少必要的参数'}, status=400)

            # 主评论查询 SQL，增加用户点赞状态
            comment_sql = '''
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
                    user_table.user_avatar AS avatar,
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
                LEFT JOIN users AS user_table ON comment.user_id = user_table.userid
                WHERE comment.is_main = '1' AND comment.reply_work_id = %s AND comment.reply_work_type = %s
                order by comment.create_time
                LIMIT %s OFFSET %s;
            '''

            # 子评论查询 SQL，增加用户点赞状态
            reply_sql = '''
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
                    user_table.user_avatar AS avatar,
                    reply_target_user_table.username AS reply_username,
                    reply_target_user_table.user_avatar AS reply_avatar,
                    reply_target_user_table.userid AS reply_user_id,
                    EXISTS(
                        SELECT 1 FROM comment_interaction 
                        WHERE comment_interaction.comment_id = reply.id 
                        AND comment_interaction.operate_user_id = %s 
                        AND comment_interaction.operate_type = 'like'
                    ) AS is_like,
                    (
                        SELECT COUNT(*) 
                        FROM comment AS all_replies 
                        WHERE all_replies.reply_comment_id = %s
                    ) AS total_reply_count
                FROM comment AS reply
                LEFT JOIN (
                    SELECT 
                        comment_interaction.comment_id AS comment_id,
                        COUNT(*) AS like_count
                    FROM comment_interaction
                    WHERE comment_interaction.operate_type = 'like'
                    GROUP BY comment_interaction.comment_id
                ) AS like_count_table ON reply.id = like_count_table.comment_id
                LEFT JOIN users AS user_table ON reply.user_id = user_table.userid
                LEFT JOIN users AS reply_target_user_table ON reply.reply_user_id = reply_target_user_table.userid
                WHERE reply.is_main = '0' AND reply.reply_comment_id = %s 
                ORDER BY reply.create_time
                LIMIT %s OFFSET %s;
            '''

            # 查询主评论
            main_comments = self.execute_sql(comment_sql, [user_id, work_id, work_type, limit, offset])

            # 查询主评论总数
            count_sql = '''
                SELECT 
                    COUNT(*) AS total
                FROM comment
                WHERE reply_work_id = %s AND reply_work_type = %s AND is_main = '1';
            '''
            total_result = self.execute_sql(count_sql, [work_id, work_type])
            total_count = total_result[0]['total'] if total_result else 0

            # 查询子评论并合并数据
            for comment in main_comments:
                comment_id = comment['comment_id']
                reply_comments = self.execute_sql(reply_sql,
                                                  [user_id, comment_id, comment_id, reply_limit, reply_offset])

                # 获取子评论总数
                total_reply_count = reply_comments[0]['total_reply_count'] if reply_comments else 0

                # 格式化子评论数据
                formatted_replies = []
                for reply in reply_comments:
                    formatted_replies.append({
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
                    })

                # 格式化主评论数据
                comment['user'] = {
                    'username': comment.pop('username', ''),
                    'avatar': comment.pop('avatar', ''),
                    'user_id': comment.pop('user_id', None)
                }
                comment['reply_list'] = formatted_replies
                comment['reply_limit'] = reply_limit
                comment['reply_offset'] = reply_offset
                comment['reply_total'] = total_reply_count  # 子评论总数
                comment['is_like'] = comment.get('is_like', False)

            # 返回结果
            return JsonResponse({
                'code': 200,
                'msg': '获取成功',
                'data': {
                    'comments': main_comments,
                    'total': total_count
                }
            })

        except Exception as exception:
            print(exception)
            self.logger.error(f"Error occurred in GetCommentList: {exception}")
            return JsonResponse({'code': 500, 'msg': '服务器内部错误'}, status=500)
