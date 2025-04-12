from django.http import JsonResponse
from base_api import BaseApi


class GetSendList(BaseApi):
    """获取发送的约稿申请"""

    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            # 登录检查
            if not request.user.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录'}, status=401)

            # 获取请求参数
            data = self.format_request(request)
            limit = int(data.get('limit', 10))
            offset = int(data.get('offset', 0))
            filter_type = data.get('filter_type', 'all')  # all, cancel
            status_filter = data.get('status_filter', None)  # 状态筛选
            sort_by = data.get('sort_by', 'time_desc')  # 排序方式

            # 基础查询条件 - 只查询约稿类型且当前用户是发起者
            conditions = [
                "type='com_an_article'",  # 约稿类型
                "user_id=%s"  # 当前用户是发起者
            ]
            params = [request.user.id]

            # 添加筛选条件
            if filter_type == 'cancel':
                conditions.append("status=0")  # 已取消的
            elif filter_type == 'all':
                pass  # 全部

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
                'time_desc': 'time DESC',  # 最新发布的在前
                'amount_desc': 'amount_of_money DESC',  # 金额高的在前
                'time_asc': 'time ASC',  # 最早发布的在前
                'status_asc': 'status ASC',  # 按状态排序
                'target_user': 'target_user_id ASC'  # 按接稿人排序
            }
            order_by = sort_mapping.get(sort_by, 'time DESC')

            # 查询SQL
            sql = f'''
            SELECT 
                id, type, amount_of_money, 
                user_id, target_user_id, 
                time, status, work_type,
                work_introduce, back, age_classification
            FROM `order`
            WHERE {where_clause}
            ORDER BY {order_by}
            LIMIT %s OFFSET %s
            '''

            # 总数SQL
            total_sql = f'''
            SELECT COUNT(*) as total FROM `order`
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
            return JsonResponse({
                'code': 500,
                'msg': '服务器错误'
            }, status=500)