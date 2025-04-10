from django.http import JsonResponse
from base_api import BaseApi


class GetReceiverList(BaseApi):
    """获取收到的约稿申请"""

    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.user.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录'}, status=401)

            data = self.format_request(request)
            limit = data.get('limit', 10)
            offset = data.get('offset', 0)
            filter_type = data.get('filter_type', 'all')  # all, cancel
            status_filter = data.get('status_filter', None)  # 状态筛选
            sort_by = data.get('sort_by', 'time_desc')  # 排序方式

            # 基础查询条件
            conditions = ["target_user_id=%s"]
            params = [request.user.id]

            # 添加筛选条件
            if filter_type == 'cancel':
                conditions.append("status=0")
            elif filter_type == 'all':
                pass  # 不添加额外条件

            # 添加状态筛选
            if status_filter and status_filter != 'all':
                try:
                    status_value = int(status_filter)
                    conditions.append("status=%s")
                    params.append(status_value)
                except ValueError:
                    pass

            # 构建WHERE子句
            where_clause = " AND ".join(conditions) if conditions else "1=1"

            # 构建排序子句
            sort_mapping = {
                'time_desc': 'time DESC',  # 最新
                'amount_desc': 'amount_of_money DESC',  # 金额从高到低
                'time_asc': 'time ASC'  # 截稿日期从早到晚(假设time是截稿日期)
            }
            order_by = sort_mapping.get(sort_by, 'time DESC')

            # 查询SQL
            sql = f'''
            SELECT * FROM admin.`order` 
            WHERE {where_clause}
            ORDER BY {order_by}
            LIMIT %s OFFSET %s
            '''

            # 总数SQL
            total_sql = f'''
            SELECT COUNT(*) as total FROM admin.`order` 
            WHERE {where_clause}
            '''

            # 执行查询
            params.extend([limit, offset])
            result = self.execute_sql(sql, params)
            total_result = self.execute_sql(total_sql, params[:-2])  # 去掉limit和offset参数

            return JsonResponse({
                'code': 200,
                'msg': '获取成功',
                'data': result,
                'total': total_result[0]['total']
            }, status=200)

        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)