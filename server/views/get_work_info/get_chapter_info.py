from base_api import BaseApi
from django.http import JsonResponse

class GetChapterInfo(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            data=self.format_request(request)
            work_id=data.get('work_id')
            chapter_id=data.get('chapter_id')
            sql='''
            select novel_content.*,novel_work.* ,novel_work.work_id as work_id,novel_content.id as chapter_id,
            users.userid as author_id
            from novel_content left join novel_work on novel_work.work_id=novel_content.belong_to_series_id
            left join users on users.userid=novel_content.belong_to_userid
             where novel_content.id=%s and belong_to_series_id =%s
            '''
            result=self.execute_sql(sql,(chapter_id,work_id))
            if result:
                return JsonResponse({'code':200,'msg':'获取成功','data':result[0]},status=200)
            else:
                return JsonResponse({'code':200,'msg':'获取失败','data':None},status=200)
        except Exception as e:
            print(e)
            self.error_log(e,request)
            return JsonResponse({'code':500,'msg':'服务器错误','data':None},status=500)