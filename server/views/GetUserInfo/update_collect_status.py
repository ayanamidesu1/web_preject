from django.http import JsonResponse
from base_api import BaseApi


class UpdateCollectStatus(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if self.check_user(request):
                return self.check_user(request)

            data = self.format_request(request)
            op_type = data.get('type')
            status = data.get('status')
            work_list = data.get('work_list')

            # 参数完整性检查
            if op_type not in ['open', 'collect']:
                return JsonResponse({'code': 400, 'msg': '参数 type 不合法'}, status=400)
            if status not in ['true', 'false']:
                return JsonResponse({'code': 400, 'msg': '参数 status 不合法'}, status=400)
            if not isinstance(work_list, list) or len(work_list) == 0:
                return JsonResponse({'code': 400, 'msg': 'work_list 参数非法或为空'}, status=400)

            # 构造 SET 子句
            set_map = {
                ('open', 'true'): 'SET is_open=1',
                ('open', 'false'): 'SET is_open=0',
                ('collect', 'true'): 'SET is_collection=1',
                ('collect', 'false'): 'SET is_collection=0'
            }
            set_str = set_map.get((op_type, status))
            if not set_str:
                return JsonResponse({'code': 400, 'msg': '操作类型与状态组合非法'}, status=400)

            sql = f'''UPDATE user_collection_table {set_str} WHERE workid=%s AND type=%s'''
            success_count = 0

            for work in work_list:
                work_id = work.get('work_id')
                work_type = work.get('work_type')
                if not work_id or not work_type:
                    continue  # 忽略非法项

                result = self.execute_sql(sql, [work_id, work_type], False)
                if result == 1:
                    success_count += 1

            if success_count == len(work_list):
                return JsonResponse({'code': 200, 'msg': '全部更新成功'}, status=200)
            elif success_count > 0:
                return JsonResponse({'code': 207, 'msg': f'部分更新成功（{success_count}/{len(work_list)}）'}, status=207)
            else:
                return JsonResponse({'code': 400, 'msg': '更新收藏状态失败'}, status=400)

        except Exception as e:
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '更新收藏状态失败，服务器错误'}, status=500)
