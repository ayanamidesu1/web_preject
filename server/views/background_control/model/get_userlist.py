from django.db import connection
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from .log.log import Logger
from datetime import datetime
import json
from .authentication import Authentication
from base_api import BaseApi

class GetUserList(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            print(request.user)
            if request.user.is_login is False or request.user.role not in ['admin','sys_admin']:
                return JsonResponse({'status': 'error', 'message': '用户未登录，或权限不足！','code':401},status=401)
            data=self.format_request(request)
            limit=data.get('limit',10)
            offset=data.get('offset',0)
            sql='''
            select * from users limit %s offset %s
            '''
            total_sql='''select count(*) as total from users'''
            result=self.execute_sql(sql,[limit,offset])
            total=self.execute_sql(total_sql)[0]['total']
            return JsonResponse({
                'status': 'success',
                'message': '获取用户列表成功！',
                'status_code': 200,
                'data': {'user_list':result},
                'total':total
            },status=200)
        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'status': 'error', 'message': '服务器错误！','code':500},status=500)




