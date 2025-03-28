from django.http import JsonResponse
from base_api import BaseApi
from djangoProject.log.log import Logger


class GetMoreReplyComment(BaseApi):
    logger = Logger()

    def post(self, request, *args, **kwargs):
        try:
            data = self.format_request(request)
            comment_id = data.get('comment_id')
            offset = data.get('offset', 0)
            limit = data.get('limit', 10)
            print(data)
            try:
                user_id = request.user.id
            except Exception as e:
                user_id = None
            if not comment_id:
                return JsonResponse({'code': 400, 'msg': '缺少 comment_id 参数'}, status=400)
            if limit <= 0 or offset < 0:
                return JsonResponse({'code': 400, 'msg': 'limit 或 offset 参数无效'}, status=400)

            sql = '''
            select comment.*,comment.id as comment_id ,users.user_id as user_id,users.username as username,users.avatar
             as user_avatar,
            EXISTS(
            select 1 from comment_interaction
            where comment_interaction.operate_user_id=%s and comment_interaction.operate_type='like' and 
            comment_interaction.comment_id=comment.id
            ) as is_like
              from comment left join users on users.user_id=comment.user_id
              LEFT JOIN (
                    SELECT 
                        comment_interaction.comment_id AS comment_id,
                        COUNT(*) AS like_count
                    FROM comment_interaction
                    WHERE comment_interaction.operate_type = 'like'
                    GROUP BY comment_interaction.comment_id
                ) AS like_count_table ON comment.id = like_count_table.comment_id
             where comment.reply_comment_id=%s 
            order by comment.create_time limit %s offset %s  
            '''
            total_sql = '''
            select count(*) as total from comment where comment.reply_comment_id=%s
            '''
            result = self.execute_sql(sql, [user_id,comment_id, limit, offset])
            result[0]['user']={
                'user_id':result[0].get('user_id', None),
                'username':result[0].get('username', None),
                'avatar':result[0].get('user_avatar', None),
            }
            total = self.execute_sql(total_sql, [comment_id])
            return JsonResponse(
                {'code': 200, 'msg': '获取成功', 'data': result, 'total': total[0].get('total', 0)}, status=200)

        except Exception as e:
            print(e)
            self.logger.error(e)
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)
