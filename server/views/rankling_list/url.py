from django.urls import path

from .model.GetRankList import GetRankList

urlpatterns=[
    path('GetRankList/',GetRankList.as_view(),name='GetRankList'),
    #获取排行榜作品及其信息的列表集
]