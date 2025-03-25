from django.urls import path

from .model.get_history import GetHistory

urlpatterns=[
    path('GetHistory/',GetHistory.as_view(),name='GetHistory'),
    #获取用户浏览记录
]