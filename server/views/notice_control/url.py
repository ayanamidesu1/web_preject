from django.urls import path
from .SearchAllNotice import NoticeOperations, ControlNoticeLogin, UserInfoByToken
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('NoticeOperations/', NoticeOperations.as_view(), name='NoticeOperations'),
    # 公告操作
    path('ControlNoticeLogin/', ControlNoticeLogin.as_view(), name='ControlNoticeLogin'),
    # 公告登录
    path('UserInfoByToken/',UserInfoByToken.as_view(),name='UserInfoByToken')
    # 通过token获取用户信息
]
