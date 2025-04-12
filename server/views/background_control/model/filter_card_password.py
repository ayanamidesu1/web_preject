from django.http import JsonResponse
from base_api import BaseApi
from datetime import datetime, timedelta


class FilterCardPassword(BaseApi):
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
            print('filter_data:', filter_data)
            # 初始化查询条件
            where_conditions = ["1=1"]  # 默认条件
            query_params = []

            # 1. 过期时间范围过滤（精确到秒）
            date_range = filter_data.get('date_range', [])
            if date_range and len(date_range) == 2:  # 添加非空检查
                try:
                    # 处理datetime-local格式 (YYYY-MM-DDTHH:MM)
                    start_date = datetime.strptime(date_range[0].replace('T', ' '), '%Y-%m-%d %H:%M')
                    end_date = datetime.strptime(date_range[1].replace('T', ' '), '%Y-%m-%d %H:%M')
                    where_conditions.append("duration BETWEEN %s AND %s")
                    query_params.extend([start_date, end_date])
                except ValueError as e:
                    return JsonResponse({
                        'code': 400,
                        'msg': f'日期格式错误，请使用 YYYY-MM-DD HH:MM 格式: {str(e)}'
                    }, status=400)

            # 2. 卡密是否过期过滤（精确到秒）
            is_expire = filter_data.get('is_expire')
            if is_expire is not None:
                current_time = datetime.now()
                if bool(is_expire):
                    where_conditions.append("(duration < %s OR duration IS NULL)")
                else:
                    where_conditions.append("duration >= %s")
                query_params.append(current_time)

            # 3. 卡密精确查询
            card_password = filter_data.get('card_key')
            if card_password:
                where_conditions.append("card_key = %s")
                query_params.append(card_password.strip())

            # 4. 使用状态过滤
            use_status = filter_data.get('use_status')
            if use_status is not None:
                where_conditions.append("use_status = %s")
                query_params.append(int(use_status))

            # 5. 价格范围过滤
            price_range = filter_data.get('price_range', {})
            min_price = float(price_range.get('min', 0))
            max_price = float(price_range.get('max', 10000))
            where_conditions.append("price BETWEEN %s AND %s")
            query_params.extend([min_price, max_price])

            # 构建完整SQL
            where_clause = " AND ".join(where_conditions)

            # 查询数据
            base_sql = f"""
                SELECT * FROM admin.card_password 
                WHERE {where_clause}
                LIMIT %s OFFSET %s
            """
            query_params.extend([limit, offset])

            results = self.execute_sql(base_sql, query_params)

            # 查询总数
            count_sql = f"""
                SELECT COUNT(*) AS total FROM admin.card_password
                WHERE {where_clause}
            """
            total = self.execute_sql(count_sql, query_params[:-2])[0]['total']

            return JsonResponse({
                'code': 200,
                'data': results,
                'total': total
            })

        except Exception as e:
            return JsonResponse({
                'code': 500,
                'msg': f'服务器错误: {str(e)}'
            }, status=500)