from django.db import connection
from django.http import JsonResponse
from django.views import View
from ..log.log import Logger
from datetime import datetime
import json
import os
import ahocorasick

sex_word_path = 'H:/web_project/djangoWebServer/Sensitive_word/sex.txt'
automaton = None  # 初始化为None


# 读取敏感词并使用Aho-Corasick算法构建自动机
def build_automaton():
    global automaton  # 使用全局变量避免重复初始化
    if automaton is None:  # 确保自动机只初始化一次
        automaton = ahocorasick.Automaton()
        with open(sex_word_path, 'r', encoding='utf-8') as f:
            for line in f:
                for word in line.strip().split(','):  # 使用逗号分隔敏感词
                    if word:
                        automaton.add_word(word, word)
        automaton.make_automaton()


class UploadNewChapter(View):
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    logger = Logger()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 构建敏感词自动机
        build_automaton()

    def request_path(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR')
        return f'{request_ip} 访问了 {request_path}，时间为 {self.now}'

    def check_sensitive_words(self, content):
        """使用Aho-Corasick算法检查内容是否包含敏感词"""
        for end_pos, word in automaton.iter(content):
            return word  # 返回找到的第一个敏感词
        return None

    def get(self, request):
        self.logger.warning(self.request_path(request) + '非法GET访问，访问请求：' + str(request.GET))
        return JsonResponse({'status': 'success', 'message': '非法GET访问，请使用POST请求！'}, status=405)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid = getattr(request, 'userid', None)
            if not userid:
                return JsonResponse({'status': 'error', 'message': 'token无效，请重新登陆'}, status=401)

            with connection.cursor() as cursor:
                cursor.execute('SELECT work_id, work_series FROM novel_work WHERE belong_to_userid = %s', [userid])
                columns = [desc[0] for desc in cursor.description]
                result = cursor.fetchall()
                if not result:
                    return JsonResponse({'status': 'error', 'message': '您还没有创建小说，请先创建小说！'}, status=401)
                rows = [dict(zip(columns, row)) for row in result]

            chapter_name = data.get('chapter_name')
            content = data.get('content')
            series_name = data.get('series_name')
            is_series = data.get('is_series')

            # 查找系列对应的 work_id
            work_id = next((row['work_id'] for row in rows if row['work_series'] == series_name), None)
            if not work_id:
                return JsonResponse({'status': 'error', 'message': '指定的系列不存在！'}, status=404)

            # 敏感词检测
            sensitive_word = self.check_sensitive_words(content)
            if sensitive_word:
                chapter_approved = 2  # 不确定，交由人工处理
            else:
                chapter_approved = 1  # 通过

            # 插入章节内容
            sql = (
                'INSERT INTO novel_content (belong_to_series_id, belong_to_userid, title, content, '
                'create_time, is_series, chapter_approved) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s)')
            with connection.cursor() as cursor:
                cursor.execute(sql, [work_id, userid, chapter_name, content, self.now, is_series, chapter_approved])
                if cursor.rowcount <= 0:
                    return JsonResponse({'status': 'error', 'message': '上传新章节失败，请重试！'}, status=500)

            return JsonResponse({'status': 'success', 'message': '上传新章节成功！'}, status=200)

        except json.JSONDecodeError as e:
            self.logger.error(self.request_path(request) + '上传新章节失败，错误信息：' + str(e))
            return JsonResponse({'status': 'error', 'message': '上传新章节失败，请重试！'}, status=500)
        except Exception as e:
            self.logger.error(self.request_path(request) + '上传新章节失败，错误信息：' + str(e))
            return JsonResponse({'status': 'error', 'message': '上传新章节失败，请重试！'}, status=500)
