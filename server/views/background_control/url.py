from django.urls import path

from .model.admin_login import AdminLogin
from .model.delete_comment import DeleteComment
from .model.edit_user_info import EditUserInfo
from .model.get_comic_list import GetComicList
from .model.get_comment_list import GetCommentList
from .model.get_ill_list import GetIllList
from .model.get_novel_content_list import GetNovelContentList
from .model.get_novel_work import GetNovelWork
from .model.get_userlist import GetUserList
from .model.search_comic import SearchComic
from .model.search_comment import SearchComment
from .model.search_ill import SearchIll
from .model.search_novel_content import SearchNovelContent
from .model.search_novel_work import SearchNovelWork
from .model.updata_ill_status import UpdateIll
from .model.update_comic_status import UpdateComic
from .model.update_comment import UpdateComment
from .model.update_novel_content import UpdateNovelContent
from .model.update_novel_work import UpdateNovelWork

urlpatterns = [
    path('AdminLogin/',AdminLogin.as_view(),name='AdminLogin'),
    #管理员登录
    path('GetUserList/',GetUserList.as_view(),name='GetUserList'),
    #获取用户列表
    path('EditUserInfo/',EditUserInfo.as_view(),name='EditUserInfo'),
    #编辑用户信息
    path('GetIllList/',GetIllList.as_view(),name='GetIllList'),
    #获取插画作品列表
    path('GetComicList/',GetComicList.as_view(),name='GetComicList'),
    #获取漫画作品列表
    path('SearchIll/',SearchIll.as_view(),name='SearchIll'),
    #搜索插画作品
    path('UpdateIll/',UpdateIll.as_view(),name='UpdateIll'),
    #更新插画作品
    path('SearchComic/',SearchComic.as_view(),name='SearchComic'),
    #搜索漫画作品
    path('UpdateComic/',UpdateComic.as_view(),name='UpdateComic'),
    #更新漫画作品
    path('GetNovelWork/',GetNovelWork.as_view(),name='GetNovelWork'),
    #获取小说作品
    path('GetNovelContentList/',GetNovelContentList.as_view(),name='GetNovelContentList'),
    #获取小说作品内容，需要指定作品ID
    path('SearchNovelWork/',SearchNovelWork.as_view(),name='SearchNovelWork'),
    #搜索小说作品
    path('SearchNovelContent/',SearchNovelContent.as_view(),name='SearchNovelContent'),
    #搜索小说内容或者章节，前提为指定小说的ID
    path('UpdateNovelWork/',UpdateNovelWork.as_view(),name='UpdateNovelWork'),
    #更新小说作品
    path('UpdateNovelContent/',UpdateNovelContent.as_view(),name='UpdateNovelContent'),
    #更新小说内容
    path('GetCommentList/',GetCommentList.as_view(),name='GetCommentList'),
    #获取评论列表
    path('SearchComment/',SearchComment.as_view(),name='SearchComment'),
    #搜索评论，支持精准搜索和模糊搜索
    path('DeleteComment/',DeleteComment.as_view(),name='DeleteComment'),
    #删除评论
    path('UpdateComment/',UpdateComment.as_view(),name='UpdateComment'),
    #更新评论
]