from django.db import connection
from django.views import  View
from django.http import JsonResponse
from ..log.log import Logger
import json

class GetUserFollowNovel(View):
    logger= Logger()
    def get(self,request,*args,**kwargs):
        return JsonResponse({'status':'success','message':'ok'})
    def post(self,request,*args,**kwargs):
        try:
            data=json.loads(request.body.decode('utf-8'))
            userid=data['userid']
            follow_user_id_list=[]
            with connection.cursor() as cursor:
                sql='select follow_user_id from user_follow where user_id=%s'
                cursor.execute(sql,[userid])
                follow_user_id_list=cursor.fetchall()
                print(follow_user_id_list)
                if not follow_user_id_list:
                    self.logger.warning(data)
                    return JsonResponse({'status':'failure','message':'No data found'},status=400)
                #获取小说信息并按照时间排序
                sql=('select * from novel_work where belong_to_userid in %s and work_approved=1 ' 
                     'ORDER BY work_create_time DESC')
                cursor.execute(sql,[tuple(follow_user_id_list)])
                columns=[desc[0] for desc in cursor.description]
                novel_result=cursor.fetchall()
                novel_list=[dict(zip(columns,row)) for row in novel_result]
                self.logger.info(novel_list)
                #获取作品列表
                return JsonResponse({'status':'success','data':novel_list})
        except Exception as e:
            self.logger.error(e)
            print(e)