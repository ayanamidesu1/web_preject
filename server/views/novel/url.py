from django.urls import path

from .upload_new_chapter import UploadNewChapter

urlpatterns = [
    path('UploadNewChapter/', UploadNewChapter.as_view(), name='UploadNewChapter'),
    # 上传新的章节
]
