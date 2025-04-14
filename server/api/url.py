from django.urls import path

from .Confirm_completion import ConfirmCompletion
from .RejectOrderCompletion import RejectOrderCompletion
from .add_func import AddFunc
from .add_order import AddOrder
from .cancel_order import CancelOrder
from .com_an_article_operate import ComAnArticleOperate
from .get_func_list import GetFuncList
from .get_order_info_by_id import GetOrderInfoById
from .get_receiver_list import GetReceiverList
from .get_self_func import GetSelfFunc
from .get_self_order import GetSelfOrder
from .get_send_list import GetSendList
from .get_send_order import GetSendOrder
from .get_target_func import GetTargetFunc
from .get_user_func_list import GetUserFuncList
from .get_wallet_info import getWalletInfo
from .init_pay_account import InitPayAccount
from .pay import OrderHandler
from .recharge import Recharge
from .complete_work import CompleteWork

# 本URL的父路径为api/，以下为具体的接口访问路径
urlpatterns = [
    path('GetSelfFunc', GetSelfFunc.as_view(), name='GetSelfFunc'),
    # 获取用户约稿方案列表
    path('GetSelfOrder', GetSelfOrder.as_view(), name='GetSelfOrder'),
    # 获取用户约稿订单列表
    path('GetTargetFunc', GetTargetFunc.as_view(), name='GetTargetFunc'),
    # 获取目标用户约稿方案列表
    path('AddFunc', AddFunc.as_view(), name='AddFunc'),
    # 添加约稿方案
    path('GetSendOrder', GetSendOrder.as_view(), name='GetSendOrder'),
    # 获取发送约稿订单列表
    path('pay', OrderHandler.as_view(), name='OrderHandler'),
    # 支付订单
    path('InitPayAccount', InitPayAccount.as_view(), name='InitPayAccount'),
    # 初始化支付账号
    path('Recharge', Recharge.as_view(), name='Recharge'),
    # 充值
    path('getWalletInfo', getWalletInfo.as_view(), name='getWalletInfo'),
    # 获取钱包信息
    path('GetFuncList', GetFuncList.as_view(), name='GetFuncList'),
    # 获取约稿方案列表
    path('GetReceiverList', GetReceiverList.as_view(), name='GetReceiverList'),
    # 获取接收到的约稿方案列表
    path('GetSendList', GetSendList.as_view(), name='GetSendList'),
    # 获取发送的约稿方案列表
    path('GetOrderInfoById', GetOrderInfoById.as_view(), name='GetOrderInfoById'),
    # 获取约稿订单信息
    path('ComAnArticleOperate', ComAnArticleOperate.as_view(), name='ComAnArticleOperate'),
    # 约稿订单操作接受或拒绝
    path('GetUserFuncList', GetUserFuncList.as_view(), name='GetUserFuncList'),
    # 获取用户约稿方案列表
    path('AddOrder', AddOrder.as_view(), name='AddOrder'),
    # 添加约稿订单
    path('CancelOrder', CancelOrder.as_view(), name='CancelOrder'),
    # 取消约稿订单
    path('CompleteWork', CompleteWork.as_view(), name='CompleteWork'),
    # 完成约稿订单
    path('ConfirmCompletion', ConfirmCompletion.as_view(), name='ConfirmCompletion'),
    # 确认完成订单
    path('RejectOrderCompletion', RejectOrderCompletion.as_view(),name='RejectOrderCompletion'),
    # 拒绝完成订单，打回重做。
]
