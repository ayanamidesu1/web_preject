from base_api import BaseApi
from django.http import JsonResponse
from datetime import datetime


class GetOrderList(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            # 管理员权限检查
            admin_check = self.check_admin(request)
            if admin_check:
                return admin_check

            # 获取请求参数
            data = self.format_request(request)
            limit = int(data.get('limit', 10))
            offset = int(data.get('offset', 0))
            filter_data = data.get('filter', {})

            # 初始化查询条件
            where_conditions = ["1=1"]  # 默认条件
            query_params = []

            # 1. 时间范围过滤 - 只有当提供两个有效时间时才应用
            time_range = filter_data.get('time_range', [])
            if time_range and len(time_range) == 2 and all(time_range):
                try:
                    start_time = datetime.strptime(time_range[0].replace('T', ' '), '%Y-%m-%d %H:%M')
                    end_time = datetime.strptime(time_range[1].replace('T', ' '), '%Y-%m-%d %H:%M')
                    where_conditions.append("time BETWEEN %s AND %s")
                    query_params.extend([start_time, end_time])
                except ValueError as e:
                    return JsonResponse({
                        'code': 400,
                        'msg': f'时间格式错误，请使用 YYYY-MM-DD HH:MM 格式: {str(e)}'
                    }, status=400)

            # 2. 订单状态过滤 - 只有当提供有效数字时才应用
            status = filter_data.get('status')
            if status is not None and str(status).strip():
                try:
                    where_conditions.append("status = %s")
                    query_params.append(int(status))
                except ValueError:
                    return JsonResponse({
                        'code': 400,
                        'msg': '订单状态必须是整数'
                    }, status=400)

            # 3. 支付类型过滤 - 只有当提供非空字符串时才应用
            payment_type = filter_data.get('type')
            if payment_type and str(payment_type).strip():
                where_conditions.append("type = %s")
                query_params.append(payment_type.strip())

            # 4. 用户ID过滤 - 只有当提供非空字符串时才应用
            user_id = filter_data.get('user_id')
            if user_id and str(user_id).strip():
                where_conditions.append("user_id = %s")
                query_params.append(user_id.strip())

            # 5. 目标用户ID过滤 - 只有当提供非空字符串时才应用
            target_user_id = filter_data.get('target_user_id')
            if target_user_id and str(target_user_id).strip():
                where_conditions.append("target_user_id = %s")
                query_params.append(target_user_id.strip())

            # 6. 金额范围过滤 - 只有当提供有效数字时才应用
            amount_range = filter_data.get('amount_range', {})
            min_amount = amount_range.get('min')
            max_amount = amount_range.get('max')

            if min_amount is not None and str(min_amount).strip():
                try:
                    min_amount = float(min_amount)
                except ValueError:
                    return JsonResponse({
                        'code': 400,
                        'msg': '最小金额必须是数字'
                    }, status=400)
            else:
                min_amount = 0  # 默认最小值

            if max_amount is not None and str(max_amount).strip():
                try:
                    max_amount = float(max_amount)
                except ValueError:
                    return JsonResponse({
                        'code': 400,
                        'msg': '最大金额必须是数字'
                    }, status=400)
            else:
                max_amount = 1000000  # 默认最大值

            where_conditions.append("amount_of_money BETWEEN %s AND %s")
            query_params.extend([min_amount, max_amount])

            # 构建完整SQL
            where_clause = " AND ".join(where_conditions)

            # 查询数据
            base_sql = f"""
                SELECT * FROM `order`
                WHERE {where_clause}
                ORDER BY time DESC
                LIMIT %s OFFSET %s
            """
            query_params.extend([limit, offset])
            results = self.execute_sql(base_sql, query_params)

            # 查询总数
            count_sql = f"""
                SELECT COUNT(*) AS total FROM `order`
                WHERE {where_clause}
            """
            total = self.execute_sql(count_sql, query_params[:-2])[0]['total']

            return JsonResponse({
                'code': 200,
                'data': results,
                'total': total
            }, status=200)

        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({
                'code': 500,
                'msg': f'服务器错误: {str(e)}'
            }, status=500)