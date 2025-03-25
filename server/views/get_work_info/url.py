from django.urls import path

from .GetChapterList import GetChapterList
from .GetComicinfo import GetComicinfo
from .GetIllInfo import GetIllInfo
from .GetNovelContent import GetNovelContent
from .GetNovelInfo import GetNovelInfo
from .GetNovelList import GetNovelList
from .SearchComicWork import SearchComicWork
from .SearchIllWork import SearchIllWork
from .SearchNovleWork import SearchNovelWork

urlpatterns = [
    path('GetIllInfo/', GetIllInfo.as_view(), name='GetIllInfo'),
    # 使用作品ID来获取作品的详细信息
    path('GetComicinfo/', GetComicinfo.as_view(), name='GetComicinfo'),
    # 使用作品ID来获取漫画作品的详细信息
    path('GetNovelList/', GetNovelList.as_view(), name='GetNovelList'),
    # 使用作品ID来获取小说作品的详细信息
    path('GetNovelContent/', GetNovelContent.as_view(), name='GetNovelContent'),
    # 使用作品ID和章节名来获取小说作品的章节内容
    path('GetNovelInfo/', GetNovelInfo.as_view(), name='GetNovelInfo'),
    #使用ID获取小说基本信息
    path('GetChapterList/', GetChapterList.as_view(), name='GetChapterList'),
    #使用ID获取章节列表
    path('SearchIllWork/', SearchIllWork.as_view(), name='SearchIllWork'),
    #为前端的插画作品搜索和作品状态筛选提供支持
    path('SearchComicWork/', SearchComicWork.as_view(), name='SearchComicWork'),
    #为前端的漫画作品搜索和作品状态筛选提供支持
    path('SearchNovelWork/', SearchNovelWork.as_view(), name='SearchNovelWork'),
    #为前端的小说作品搜索和作品状态筛选提供支持
]
