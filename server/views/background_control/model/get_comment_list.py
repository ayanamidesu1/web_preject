from django.http import JsonResponse
from base_api import BaseApi

class GetCommentList(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            # 权限验证（与样例完全一致的验证方式）
            if request.user.is_login is False or request.user.role not in ['admin', 'sys_admin']:
                return JsonResponse(
                    {'status': 'error', 'code': 403, 'message': '权限不足', 'msg': '权限不足', 'data': None},
                    status=403
                )

            # 使用基类方法格式化请求数据
            data = self.format_request(request)
            limit = data.get('limit', 10)
            offset = data.get('offset', 0)

            # 主评论查询（保持样例SQL缩进风格）
            main_sql = '''
                SELECT 
                    comment.*,
                    users.userid,
                    users.username,
                    users.user_avatar
                FROM comment
                LEFT JOIN users ON users.userid = comment.user_id
                ORDER BY comment.create_time DESC
                LIMIT %s OFFSET %s
            '''
            comments = self.execute_sql(main_sql, (limit, offset), return_results=True)

            # 获取关联作品数据
            for comment in comments:
                work_type = comment.get('work_type')
                work_id = comment.get('work_id')
                comment['work_data'] = self._get_work_details(work_type, work_id)

            # 总数查询（保持样例风格）
            count_sql = "SELECT COUNT(*) AS total FROM comment"
            total = self.execute_sql(count_sql, return_results=True)[0]['total']

            # 保持完全一致的响应结构
            return JsonResponse({
                'status': 'success',
                'code': 200,
                'message': '请求成功',
                'msg': '请求成功',
                'data': {
                    'comment_list': comments,
                    'total': total
                }
            }, status=200)

        except Exception as e:
            # 保持完全相同的错误处理方式
            print(f'[COMMENT API ERROR] {str(e)}')
            self.error_log(e, request)
            return JsonResponse(
                {'status': 'error', 'code': 500, 'message': '服务器错误', 'msg': '服务器错误', 'data': None},
                status=500
            )

    def _get_work_details(self, work_type: str, work_id: int) -> dict:
        """统一获取作品详情（使用基类方法）"""
        type_mapping = {
            'ill': ('illustration_work', 'Illustration_id'),
            'comic': ('comic', 'id'),
            'novel': ('novel_work', 'work_id')
        }

        if work_type not in type_mapping:
            return {}

        table_name, id_field = type_mapping[work_type]
        sql = f'''
            SELECT * 
            FROM {table_name}
            WHERE {id_field} = %s
            LIMIT 1
        '''
        result = self.execute_sql(sql, (work_id,), return_results=True)
        return result[0] if result else {}