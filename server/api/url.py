from django.urls import path

from .add_func import AddFunc
from .get_func_list import GetFuncList
from .get_receiver_list import GetReceiverList
from .get_self_func import GetSelfFunc
from .get_self_order import GetSelfOrder
from .get_send_order import GetSendOrder
from .get_target_func import GetTargetFunc
from .get_wallet_info import getWalletInfo
from .init_pay_account import InitPayAccount
from .pay import OrderHandler
from .recharge import Recharge
#本URL的父路径为api/，以下为具体的接口访问路径
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
    path('pay',OrderHandler.as_view(),name='OrderHandler'),
    # 支付订单
    path('InitPayAccount',InitPayAccount.as_view(),name='InitPayAccount'),
    # 初始化支付账号
    path('Recharge',Recharge.as_view(),name='Recharge'),
    # 充值
    path('getWalletInfo',getWalletInfo.as_view(),name='getWalletInfo'),
    # 获取钱包信息
    path('GetFuncList',GetFuncList.as_view(),name='GetFuncList'),
    # 获取约稿方案列表
    path('GetReceiverList',GetReceiverList.as_view(),name='GetReceiverList'),
    # 获取接收到的约稿方案列表
]