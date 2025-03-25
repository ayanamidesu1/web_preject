from django.urls import path

from .DeleteUserBack import DeleteUserBack
from .UpdateUserBack import UpdateUserBack
from .UpdateUserCollect import UpdateUserCollect
from .UpdateUserInfo import UpdateUserInfo
from .UpdateUserSelectWork import UpdateUserSelectWork

urlpatterns=[
 path('UpdateUserBack/',UpdateUserBack.as_view(),name='UpdateUserBack'),
    #更新用户的背景
 path('DeleteUserBack/',DeleteUserBack.as_view(),name='DeleteUserBack'),
 #删除用户的背景,替换为默认背景
 path('UpdateUserInfo/',UpdateUserInfo.as_view(),name='UpdateUserInfo'),
 #更新用户的信息
 path('UpdateUserSelectWork/',UpdateUserSelectWork.as_view(),name='UpdateUserSelectWork'),
 #更新用户选择的作品
 path('UpdateUserCollect/',UpdateUserCollect.as_view(),name='UpdateUserCollect'),
 #更新用户收藏的作品状态或者删除收藏
]