from django.http import JsonResponse
from base_api import BaseApi

class GetNovelWork(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            # 管理员权限验证（与样例保持完全一致）
            if request.user.is_login is False or request.user.role not in ['admin', 'sys_admin']:
                return JsonResponse(
                    {'status': 'error', 'code': 403, 'message': '权限不足', 'msg': '权限不足', 'data': None},
                    status=403
                )

            # 使用基类方法获取请求参数
            data = self.format_request(request)
            limit = data.get('limit', 10)
            offset = data.get('offset', 0)

            # 数据查询（保持样例的SQL缩进风格）
            list_sql = '''
                SELECT 
                    novel_work.*,
                    users.userid,
                    users.user_avatar,
                    users.username,
                    SUM(CHAR_LENGTH(novel_content.content)) AS novel_word_count
                FROM novel_work
                LEFT JOIN users ON users.userid = novel_work.belong_to_userid
                LEFT JOIN novel_content ON novel_content.belong_to_series_id = novel_work.work_id
                GROUP BY novel_work.work_id
                ORDER BY novel_work.time DESC
                LIMIT %s OFFSET %s
            '''
            result = self.execute_sql(list_sql, (limit, offset), return_results=True)

            # 总数查询（保持样例风格）
            total_sql = "SELECT COUNT(*) AS total FROM novel_work"
            total = self.execute_sql(total_sql, return_results=True)[0]['total']

            # 保持完全一致的响应结构
            return JsonResponse({
                'status': 'success',
                'code': 200,
                'message': '请求成功',
                'msg': '请求成功',
                'data': {
                    'work_list': result,
                    'total': total
                }
            }, status=200)

        except Exception as e:
            # 保持完全相同的错误处理方式
            print(f'[ERROR] {str(e)}')
            self.error_log(e, request)
            return JsonResponse(
                {'status': 'error', 'code': 500, 'message': '服务器错误', 'msg': '服务器错误', 'data': None},
                status=500
            )