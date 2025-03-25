from django.db import connection
from django.http import  JsonResponse
from django.views import  View
import  json
from ..log.log import  Logger

class GetUserFollowToComic(View):

    logger=Logger()
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
                #获取漫画信息并按照时间排序
                sql=('select * from comic where comic.belong_to_userid in %s and comic.work_approved=1 ' 
                     'ORDER BY create_time DESC')
                cursor.execute(sql,[tuple(follow_user_id_list)])
                columns=[desc[0] for desc in cursor.description]
                comic_result=cursor.fetchall()
                comic_list=[dict(zip(columns,row)) for row in comic_result]
                self.logger.info(comic_list)
                print(comic_list)
                #获取作品列表
                return JsonResponse({'status':'success','data':comic_list})
        except Exception as e:
            self.logger.error(e)
            print(e)