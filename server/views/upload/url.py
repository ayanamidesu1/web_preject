from django.urls import path

from .GetPreviewCover import GetPreviewCover
from .UploadNewSeries import UploadNewSeries
from .upload import UploadFile

urlpatterns = [
    path('UploadFile/', UploadFile.as_view(), name='UploadFile'),
    # 上传文件接口
    path('GetPreviewCover/', GetPreviewCover.as_view(), name='GetPreviewCover'),
    # 获取预览封面接口
    path('UploadNewSeries/', UploadNewSeries.as_view(), name='UploadNewSeries'),
    # 上传新系列接口
]
