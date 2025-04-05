from django.urls import path

from .add_func import AddFunc
from .get_self_func import GetSelfFunc
from .get_self_order import GetSelfOrder
from .get_send_order import GetSendOrder
from .get_target_func import GetTargetFunc

urlpatterns=[
    path('GetSelfFunc',GetSelfFunc.as_view(),name='GetSelfFunc'),
    # 获取用户约稿方案列表
    path('GetSelfOrder',GetSelfOrder.as_view(),name='GetSelfOrder'),
    # 获取用户约稿订单列表
    path('GetTargetFunc',GetTargetFunc.as_view(),name='GetTargetFunc'),
    # 获取目标用户约稿方案列表
    path('AddFunc',AddFunc.as_view(),name='AddFunc'),
    # 添加约稿方案
    path('GetSendOrder',GetSendOrder.as_view(),name='GetSendOrder'),
    # 获取发送约稿订单列表

]