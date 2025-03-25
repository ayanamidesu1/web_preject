from .GetAllUserInfo import GetAllUserInfo
from django.urls import path

from .GetFriendList import GetFriendList
from .GetGroupList import GetGroupList, GroupControlInfo, GetGroupInfo
from .GetSearch import GetSearch
from .GetUserCollect import GetUserCollect
from .GetUserFans import GetUserFans
from .GetUserFollow import GetUserFollow
from .GetUserFollowList import GetUserFollowList, UserAddFollow
from .GetUserFollowNovel import GetUserFollowNovel
from .GetUserFollowToComic import GetUserFollowToComic
from .GetUserFollowToIll import GetUserFollowToIll
from .GetUserFollowWorkTags import GetUserFollowWorkTags
from .GetUserHistoryMsg import GetUserHistoryMsg
from .GetUserWorkList import GetUserWorkList
from .GetUserWorkSeries import GetUserWorkSeries
from .GroupControl import GroupControl
from .login import Login

urlpatterns = [
    path('GetAllUserInfo/', GetAllUserInfo.as_view(), name='GetAllUserInfo'),
    # 使用ID获取用户信息
    path('Login/', Login.as_view(), name='Login'),
    # 用户登录接口
    path('GetUserFans/', GetUserFans.as_view(), name='GetUserFans'),
    # 获取用户粉丝
    path('GetUserFollow/', GetUserFollow.as_view(), name='GetUserFollow'),
    # 获取用户关注
    path('GetUserFollowToIll/', GetUserFollowToIll.as_view(), name='GetUserFollowToIll'),
    # 获取用户关注的用户的插画详情
    path('GetUserFollowToComic/', GetUserFollowToComic.as_view(), name='GetUserFollowToComic'),
    # 获取用户关注的用户的漫画详情
    path('GetUserFollowNovel/', GetUserFollowNovel.as_view(), name='GetUserFollowNovel'),
    # 获取用户关注的用户的小说详情
    path('GetFriendList/', GetFriendList.as_view(), name='GetFriendList'),
    # 获取用户的好友列表
    path('GetUserHistoryMsg/', GetUserHistoryMsg.as_view(), name='GetUserHistoryMsg'),
    # 获取用户的历史消息
    path('GetGroupList/', GetGroupList.as_view(), name='GetGroupList'),
    # 获取群组列表
    path('GroupControlInfo/', GroupControlInfo.as_view(), name='GroupControlInfo'),
    # 获取群组管理权限信息
    path('GroupControl/', GroupControl.as_view(), name='GroupControl'),
    # 群管理
    path('GetGroupInfo/', GetGroupInfo.as_view(), name='GetGroupInfo'),
    # 获取群组信息
    path('GetSearch/', GetSearch.as_view(), name='GetSearch'),
    # 作品查询/搜索
    path('GetUserWorkList/', GetUserWorkList.as_view(), name='GetUserWorkList'),
    # 获取用户所有的作品列表
    path('GetUserFollowList/', GetUserFollowList.as_view(), name='GetUserFollowList'),
    # 获取用户关注的用户用户列表
    path('UserAddFollow/', UserAddFollow.as_view(), name='UserAddFollow'),
    # 用户关注
    path('GetUserWorkSeries/', GetUserWorkSeries.as_view(), name='GetUserWorkSeries'),
    # 获取用户的作品系列
    path('GetUserCollect/',GetUserCollect.as_view(),name='GetUserCollect'),
    # 获取用户的收藏列表及其作者信息
    path('GetUserFollowWorkTags/',GetUserFollowWorkTags.as_view(),name='GetUserFollowWorkTags'),
    # 获取用户关注的用户的作品标签
]
