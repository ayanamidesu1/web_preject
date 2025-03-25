from django.db import connection
from django.views import View
from django.http import JsonResponse
from ..log.log import Logger
from django.shortcuts import render
import json
from datetime import datetime

class GetChapterList(View):
    logger = Logger()
    def request_path(self,request):
        request_path=request.path
        request_ip=request.META['REMOTE_ADDR']
        now=datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        return f'{request_ip}在{now}请求了{request_path}'

    def get(self,request):
        self.logger.warning(self.request_path(request)+'非法GET请求；请求内容为：'+str(request.GET))
        return render(request,'404.html',status=404)

    def post(self,request,*args,**kwargs):
        userid=getattr(request,'userid',None)
        if userid is None:
            self.logger.warning(self.request_path(request)+'用户未登录')
            return JsonResponse({'status':'success','message':'用户未登录'},status=401)
        try:
            data=json.loads(request.body.decode('utf-8'))
            work_id=data.get('work_id',None)
            if not work_id:
                self.logger.warning(self.request_path(request)+'缺少参数work_id')
                return JsonResponse({'status':'error','message':'缺少参数work_id'},status=400)
            if work_id:
                with connection.cursor() as cursor:
                    sql="""
                        select * from novel_content where belong_to_series_id=%s 
                    """
                    cursor.execute(sql,[work_id])
                    result=cursor.fetchall()
                    if not result:
                        return JsonResponse({'status':'error','message':'该作品不存在'},status=400)
                    columns=[column[0] for column in cursor.description]
                    rows=[dict(zip(columns,row)) for row in result]
                    return JsonResponse({'status':'success','message':'查询成功','data':rows},status=200)

        except Exception as e:
            print(e)
            self.logger.error(self.request_path(request)+'发生错误：'+str(e))
            return JsonResponse({'status':'error','message':'服务器内部错误'},status=500)